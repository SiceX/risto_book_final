from django.shortcuts import render
from django.views.generic import ListView

from menu.models import Piatto


class PiattoList(ListView):
	model = Piatto
	template_name = 'menu/piatto/list.html'
