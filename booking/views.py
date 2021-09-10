import datetime
import logging
from collections import Counter
from functools import partial

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.forms import DateInput
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from django.views.generic.edit import FormMixin, DeleteView
from django.utils.timezone import make_aware
from extra_views import ModelFormSetView
from typing import Tuple

from booking.forms import DateNavForm, PrenotazioneForm
from booking.models import Tavolo, Prenotazione

_logger = logging.getLogger(__name__)


class TavoloCreate(CreateView):
	model = Tavolo
	template_name = 'booking/tavolo/create.html'
	fields = ['nome', 'abilitato']
	success_url = reverse_lazy('booking:tavolo-list')


class TavoloDetail(DetailView):
	model = Tavolo
	template_name = 'booking/tavolo/detail.html'


class TavoloList(ListView):
	model = Tavolo
	template_name = 'booking/tavolo/list.html'


class PrenotazioneList(LoginRequiredMixin, ListView):
	model = Prenotazione
	template_name = 'booking/prenotazione/list.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(utente=self.request.user)


class PrenotazioneDelete(LoginRequiredMixin, DeleteView):
	model = Prenotazione
	template_name = 'booking/prenotazione/delete.html'
	success_url = reverse_lazy('booking:prenotazione-list')

	def delete(self, *args, **kwargs):
		self.object = self.get_object()
		success_url = self.get_success_url()
		prenotazioni_in_coda = Prenotazione.objects\
			.filter(data_ora=self.object.data_ora, tavolo=self.object.tavolo)\
			.exclude(utente=self.object.utente)
		self.object.delete()

		# Dopo aver eliminato la prenotazione, decremento i segna-posto della lista d'attesa, se ce ne sono
		if prenotazioni_in_coda is not None:
			prenotazioni_in_coda.update(queue_place=F('queue_place')-1)

		return HttpResponseRedirect(success_url)


class PrenotazioneCreate(LoginRequiredMixin, CreateView):
	model = Prenotazione
	template_name = 'booking/prenotazione/create.html'
	success_url = reverse_lazy('home')
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
		data_ora = make_aware(datetime.datetime(year, month, day, hour))
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


class DashboardPrenotazioni(ListView, FormMixin):
	model = Tavolo
	template_name = 'booking/prenotazione/dashboard_prenotazioni.html'
	form_class = DateNavForm

	year = None
	month = None
	day = None

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

		num_tavoli = Tavolo.objects.count()
		year = self.kwargs["year"]
		month = self.kwargs["month"]
		day = self.kwargs["day"]
		user_id = self.request.user.id

		# Creo due liste con gli id dei tavoli prenotati, uno per pranzo e uno per cena.
		# Mi segno anche due contatori delle eventuali persone in coda, uno a pranzo ed uno a cena

		lookup_date = make_aware(datetime.datetime(year, month, day, 12))
		ctx['prenotati_pranzo'], ctx['in_coda_pranzo'], ctx['has_already_booked_pranzo'] = \
			self.get_bookings_data(lookup_date, user_id)

		lookup_date = make_aware(datetime.datetime(year, month, day, 19))
		ctx['prenotati_cena'],	ctx['in_coda_cena'], ctx['has_already_booked_cena'] = \
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
			prenotati = Prenotazione.objects.filter(data_ora=lookup_date_hour).values_list('tavolo_id', flat=True)
		except ObjectDoesNotExist:
			prenotati = {}
		in_coda = get_available_queue_place(lookup_date_hour)

		has_already_booked = None
		if user_id is not None:
			has_already_booked = Prenotazione.objects.filter(data_ora=lookup_date_hour, utente=user_id).exists()

		return prenotati, in_coda, has_already_booked


def get_available_queue_place(lookup_date_hour) -> int:
	"""
	Ritorna il posto in coda che riceverebbe una nuova prenotazione per il dato orario
	@param lookup_date_hour: datetime.datetime della data e ora da andare a guardare
	@return: posto in coda, calcolato come numero di tavoli abilitati meno numero di prenotazioni nel dato orario.
			Può essere negativo, nel qual caso vuol dire che ci sono ancora tavoli liberi.
	"""
	num_tavoli = Tavolo.objects.filter(abilitato=True).count()
	num_prenotazioni = Prenotazione.objects.filter(data_ora=lookup_date_hour).count()
	return num_prenotazioni - num_tavoli
