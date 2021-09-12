from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from extra_views import ModelFormSetView

from admin_tools import forms
from admin_tools.forms import GestisciTavoliForm
from booking.models import Tavolo


class TavoloCreate(LoginRequiredMixin, CreateView):
	model = Tavolo
	template_name = 'admin_tools/tavolo/create.html'
	fields = ['nome', 'abilitato']
	success_url = reverse_lazy('admin_tools:tavolo-list')


class TavoloDelete(LoginRequiredMixin, DeleteView):
	model = Tavolo
	template_name = 'admin_tools/tavolo/delete.html'
	success_url = reverse_lazy('admin_tools:tavolo-manage-list')

	def delete(self, *args, **kwargs):
		self.object = self.get_object()
		success_url = self.get_success_url()
		self.object.delete()

		return HttpResponseRedirect(success_url)


class TavoloDetail(LoginRequiredMixin, DetailView):
	model = Tavolo
	template_name = 'admin_tools/tavolo/detail.html'


class TavoloList(LoginRequiredMixin, ListView):
	model = Tavolo
	template_name = 'admin_tools/tavolo/list.html'


class TavoloListAndUpdate(LoginRequiredMixin, ModelFormSetView):
	model = Tavolo
	template_name = 'admin_tools/tavolo/updateList.html'
	form_class = GestisciTavoliForm
