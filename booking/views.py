import datetime
import logging
from functools import partial

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.forms import DateInput
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from django.views.generic.edit import FormMixin
from django.utils.timezone import make_aware
from extra_views import ModelFormSetView

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


class PrenotazioneCreate(LoginRequiredMixin, CreateView):
	model = Prenotazione
	template_name = 'booking/prenotazione/create.html'
	success_url = reverse_lazy('home')
	form_class = PrenotazioneForm

	def get_initial(self):
		year = self.kwargs["year"]
		month = self.kwargs["month"]
		day = self.kwargs["day"]
		hour = self.kwargs["hour"]
		data_ora = make_aware(datetime.datetime(year, month, day, hour))
		return {'tavolo': self.kwargs["tavolo"], 'data_ora': data_ora}

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

		year = self.kwargs["year"]
		month = self.kwargs["month"]
		day = self.kwargs["day"]

		lookup_date = make_aware(datetime.datetime(year, month, day, 12))
		try:
			prenotati_pranzo = Prenotazione.objects.filter(data_ora=lookup_date).values_list('tavolo_id', flat=True)
		except ObjectDoesNotExist:
			prenotati_pranzo = []

		lookup_date = make_aware(datetime.datetime(year, month, day, 19))
		try:
			prenotati_cena = Prenotazione.objects.filter(data_ora=lookup_date).values_list('tavolo_id', flat=True)
		except ObjectDoesNotExist:
			prenotati_cena = []

		ctx['prenotati_pranzo'] = prenotati_pranzo
		ctx['prenotati_cena'] = prenotati_cena

		return ctx
