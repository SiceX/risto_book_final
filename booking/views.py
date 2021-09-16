import logging
from datetime import datetime, timedelta
from typing import Tuple

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.generic import ListView, CreateView, RedirectView
from django.views.generic.edit import FormMixin, DeleteView

from booking.forms import DateNavForm, PrenotazioneForm
from booking.models import Tavolo, Prenotazione

_logger = logging.getLogger(__name__)


class PrenotazioneList(LoginRequiredMixin, ListView):
	model = Prenotazione
	template_name = 'booking/prenotazione/list.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(utente=self.request.user,  data_ora__gte=timezone.now())


class PrenotazioneDelete(LoginRequiredMixin, DeleteView):
	model = Prenotazione
	template_name = 'booking/prenotazione/delete.html'
	success_url = reverse_lazy('booking:prenotazione-list')

	def delete(self, *args, **kwargs):
		self.object = self.get_object()
		success_url = self.get_success_url()
		prenotazioni_in_coda = Prenotazione.objects.filter(data_ora=self.object.data_ora,
														   queue_place__isnull=False).order_by('queue_place')
		tavolo_liberato_id = self.object.tavolo_id
		queue_place_liberato = self.object.queue_place
		self.object.delete()

		# Dopo aver eliminato la prenotazione, decremento i segna-posto della lista d'attesa e assegno il tavolo al primo
		if prenotazioni_in_coda.exists():
			if tavolo_liberato_id is not None:
				next_user = prenotazioni_in_coda.filter(queue_place=0).get().utente
				PrenotazioneDelete.notify_next_in_line(next_user.email, tavolo_liberato_id, self.object.data_ora)

				prenotazioni_in_coda.filter(queue_place=0).update(tavolo_id=tavolo_liberato_id, queue_place=None)
				prenotazioni_in_coda.filter(queue_place__gt=0).update(queue_place=F('queue_place') - 1)
			elif queue_place_liberato is not None:
				prenotazioni_in_coda.filter(queue_place__gt=queue_place_liberato).update(
					queue_place=F('queue_place') - 1)

		return HttpResponseRedirect(success_url)

	@staticmethod
	def notify_next_in_line(email, tavolo, data_ora):
		"""
		Non funziona davvero, perché non ho a mia disposizione un server SMTP da usare (e non mi ispira dover diminuire
		la sicurezza dei miei account gmail), però dovrebbe inviare una mail di notifica all'utente che ha appena vinto
		un tavolo appena liberato.
		@param email: email dell'utente da notificare
		@param tavolo: id/nome del tavolo appena assegnato
		@param data_ora: datetime.datetime della prenotazione
		"""
		send_mail(
			'Nuovo tavolo assegnato',
			'Gentile cliente, un tavolo si è liberato!\n'
			f'Le è stato assegnato il tavolo {tavolo} per la prenotazione delle {data_ora}.',
			'noreply@ristobooking.com',
			[email],
			fail_silently=True,
		)


class PrenotazioneCreate(LoginRequiredMixin, CreateView):
	model = Prenotazione
	template_name = 'booking/prenotazione/create.html'
	success_url = reverse_lazy('booking:prenotazione-list')
	form_class = PrenotazioneForm

	def get_initial(self):
		# Se tavolo non è stato impostato, vuol dire che è una prenotazione per mettersi in coda
		if "tavolo" in self.kwargs:
			tavolo = self.kwargs["tavolo"]
		else:
			tavolo = None
		year = self.kwargs["year"]
		month = self.kwargs["month"]
		day = self.kwargs["day"]
		hour = self.kwargs["hour"]
		data_ora = make_aware(datetime(year, month, day, hour))
		# Il posto nella coda di una nuova prenotazione equivale al numero di prenotazioni in coda attuali
		queue_place = get_available_queue_place(data_ora)
		if queue_place >= 0:
			return {'data_ora': data_ora, 'queue_place': queue_place}
		else:
			return {'tavolo': tavolo, 'data_ora': data_ora}

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.utente = self.request.user
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())


def dashboard_prenotazioni_controller(request, year, month, day):
	kwargs = {'year': year, 'month': month, 'day': day}
	date = datetime(year, month, day)
	if date.date() < (timezone.now().date() + timedelta(days=1)):
		tomorrow = datetime.now().date() + timedelta(days=1)
		return redirect('booking:dashboard-prenotazioni', tomorrow.year, tomorrow.month, tomorrow.day)
	return DashboardPrenotazioni.as_view()(request, **kwargs)


class DashboardPrenotazioni(ListView, FormMixin):
	model = Tavolo
	template_name = 'booking/prenotazione/dashboard_prenotazioni.html'
	form_class = DateNavForm

	year = None
	month = None
	day = None

	def get_initial(self):
		date = datetime(self.kwargs["year"], self.kwargs["month"], self.kwargs["day"])
		return {'datetime': date.strftime("%Y %m %d")}

	def get_success_url(self):
		return reverse_lazy('booking:dashboard-prenotazioni', kwargs={
			'year': self.year,
			'month': self.month,
			'day': self.day
		})

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		selected_date = form.cleaned_data["data"]
		self.year = selected_date.year
		self.month = selected_date.month
		self.day = selected_date.day
		return super().form_valid(form)

	def form_invalid(self, request, *args, **kwargs):
		return self.get(self, request, *args, **kwargs)

	def get_queryset(self):
		return Tavolo.objects.filter(abilitato=True)

	def get_context_data(self, **kwargs):
		ctx = super(DashboardPrenotazioni, self).get_context_data(**kwargs)

		year = self.kwargs["year"]
		month = self.kwargs["month"]
		day = self.kwargs["day"]
		user_id = self.request.user.id

		# Creo due liste con gli id dei tavoli prenotati, uno per pranzo e uno per cena.
		# Mi segno anche due contatori delle eventuali persone in coda, uno a pranzo ed uno a cena

		lookup_date = make_aware(datetime(year, month, day, 12))
		ctx['prenotati_pranzo'], ctx['in_coda_pranzo'], ctx['has_already_booked_pranzo'] = \
			self.get_bookings_data(lookup_date, user_id)

		lookup_date = make_aware(datetime(year, month, day, 19))
		ctx['prenotati_cena'], ctx['in_coda_cena'], ctx['has_already_booked_cena'] = \
			self.get_bookings_data(lookup_date, user_id)

		return ctx

	@staticmethod
	def get_bookings_data(lookup_date_hour, user_id=None) -> Tuple[list, int, bool]:
		"""
		Ritorna la lista di tavoli prenotati e numero di prenotazioni totali per quella data-ora
		@param lookup_date_hour: datetime.datetime della data e ora da andare a guardare
		@param user_id: opzionale, per controllare se l'utente ha già una prenotazione nel dato orario.
		@return: Tupla con:
		-lista di tavoli prenotati;
		-numero di persone in coda, può essere negativo se ci sono ancora tavoli liberi;
		-booleano, vero se l'utente ha già prenotazione per il dato orario, None se user_id non specificato.
		"""
		try:
			prenotati = Prenotazione.objects.filter(data_ora=lookup_date_hour, tavolo__abilitato=True).\
				values_list('tavolo_id', flat=True)
		except ObjectDoesNotExist:
			prenotati = {}
		in_coda = get_available_queue_place(lookup_date_hour)

		has_already_booked = None
		if user_id is not None:
			has_already_booked = Prenotazione.objects.filter(data_ora=lookup_date_hour, utente=user_id).exists()

		return prenotati, in_coda, has_already_booked


class FindFirstFreeDayRedirectView(RedirectView):
	permanent = False
	query_string = False
	pattern_name = 'booking:dashboard-prenotazioni'

	def get_redirect_url(self, *args, **kwargs):
		start_date = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0) + timedelta(days=1)
		for single_date in (start_date + timedelta(days=n) for n in range(30)):
			kwargs = {"year": single_date.strftime('%Y'),
					 "month": single_date.strftime('%m'),
					 "day": single_date.strftime('%d')}

			pranzo_queue_status = get_available_queue_place(single_date)
			if pranzo_queue_status < 0:
				return super().get_redirect_url(*args, **kwargs)

			single_date = single_date.replace(hour=19)
			cena_queue_status = get_available_queue_place(single_date)
			if cena_queue_status < 0:
				return super().get_redirect_url(*args, **kwargs)


class FindFirstFreeDayForTableRedirectView(RedirectView):
	permanent = False
	query_string = False
	pattern_name = 'booking:dashboard-prenotazioni'

	def get_redirect_url(self, *args, **kwargs):
		tavolo_id = kwargs['tavolo']
		start_date = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0) + timedelta(days=1)
		for single_date in (start_date + timedelta(days=n) for n in range(30)):
			kwargs = {"year": single_date.strftime('%Y'),
					 "month": single_date.strftime('%m'),
					 "day": single_date.strftime('%d')}

			if not is_tavolo_prenotato(single_date, tavolo_id):
				return super().get_redirect_url(*args, **kwargs)

			single_date = single_date.replace(hour=19)
			if not is_tavolo_prenotato(single_date, tavolo_id):
				return super().get_redirect_url(*args, **kwargs)


def get_available_queue_place(lookup_date_hour) -> int:
	"""
	Ritorna il posto in coda che riceverebbe una nuova prenotazione per il dato orario
	@param lookup_date_hour: datetime.datetime della data e ora da andare a guardare
	@return: posto in coda, calcolato come numero di tavoli abilitati meno numero di prenotazioni nel dato orario.
			Può essere negativo, nel qual caso vuol dire che ci sono ancora tavoli liberi.
	"""
	num_tavoli = Tavolo.objects.filter(abilitato=True).count()
	num_prenotazioni = Prenotazione.objects.filter(data_ora=lookup_date_hour, tavolo__abilitato=True).count()
	return num_prenotazioni - num_tavoli


def is_tavolo_prenotato(lookup_date_hour, tavolo) -> bool:
	return Prenotazione.objects.filter(data_ora=lookup_date_hour, tavolo_id=tavolo).exists()
