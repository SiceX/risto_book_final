from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from extra_views import ModelFormSetView

from booking.models import Tavolo


class TavoloCreate(CreateView):
	model = Tavolo
	template_name = 'admin_tools/tavolo/create.html'
	fields = ['nome', 'abilitato']
	success_url = reverse_lazy('admin_tools:tavolo-list')


class TavoloDetail(DetailView):
	model = Tavolo
	template_name = 'admin_tools/tavolo/detail.html'


class TavoloList(ListView):
	model = Tavolo
	template_name = 'admin_tools/tavolo/list.html'


class TavoloListAndUpdate(ModelFormSetView):
	model = Tavolo
	fields = ['nome', 'abilitato']
	template_name = 'admin_tools/tavolo/updateList.html'
	# form_class = forms
