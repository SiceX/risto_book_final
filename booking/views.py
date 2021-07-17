import logging
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from booking.models import Tavolo

_logger = logging.getLogger(__name__)


class TavoloDetail(DetailView):
	model = Tavolo
	template_name = 'booking/tavolo/detail.html'
