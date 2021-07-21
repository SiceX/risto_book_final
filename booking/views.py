import datetime
import logging

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView
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


class DashboardPrenotazioni(ListView):
	model = Tavolo
	template_name = 'booking/prenotazione/dashboard_prenotazioni.html'
	year = None
	month = None
	day = None
	hour = None

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


# class TavoloAbilitateList(ModelFormSetView):
# 	model = Tavolo
# 	template_name = 'booking/tavolo/updateList.html'
# 	#form_class = forms.EditListForm
