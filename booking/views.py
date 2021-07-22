import datetime
import logging
from functools import partial

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import DateInput
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from django.views.generic.edit import FormMixin
from extra_views import ModelFormSetView

from booking.models import Tavolo, Prenotazione

_logger = logging.getLogger(__name__)


class TavoloCreate(CreateView):
	model = Tavolo
	template_name = 'booking/tavolo/create.html'
	fields = ['nome', 'stato']
	success_url = reverse_lazy('booking:tavolo-list')


class TavoloDetail(DetailView):
	model = Tavolo
	template_name = 'booking/tavolo/detail.html'


class TavoloList(ListView):
	model = Tavolo
	template_name = 'booking/tavolo/list.html'


class DateNavForm(forms.Form):
	selected_date = forms.DateTimeField(widget=DateInput())


class DashboardPrenotazioni(ListView, FormMixin):
	model = Tavolo
	template_name = 'booking/prenotazione/dashboard_prenotazioni.html'
	form_class = DateNavForm

	year = None
	month = None
	day = None
	hour = None

	def get_success_url(self):
		return reverse_lazy('booking:dashboard-prenotazioni', kwargs={
			'year': self.year,
			'month': self.month,
			'day': self.day,
			'hour': self.hour
		})

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		selected_date = form.cleaned_data["selected_date"]
		self.year = selected_date.year
		self.month = selected_date.month
		self.day = selected_date.day
		self.hour = 12
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		ctx = super(DashboardPrenotazioni, self).get_context_data(**kwargs)

		year = self.kwargs["year"]
		month = self.kwargs["month"]
		day = self.kwargs["day"]
		hour = self.kwargs["hour"]
		lookup_date = datetime.datetime(year, month, day, hour)

		try:
			tavoli_prenotati = Prenotazione.objects.filter(data_ora=lookup_date).values_list('tavolo_id', flat=True)
		except ObjectDoesNotExist:
			tavoli_prenotati = []

		ctx['tavoli_prenotati'] = tavoli_prenotati

		return ctx
