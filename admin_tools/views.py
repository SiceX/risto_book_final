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
		# prenotazioni_in_coda = Prenotazione.objects.filter(data_ora=self.object.data_ora,
		# 												   queue_place__isnull=False).order_by('queue_place')
		# tavolo_liberato_id = self.object.tavolo_id
		# queue_place_liberato = self.object.queue_place
		# self.object.delete()
		#
		# # Dopo aver eliminato la prenotazione, decremento i segna-posto della lista d'attesa e assegno il tavolo al primo
		# if prenotazioni_in_coda.exists():
		# 	if tavolo_liberato_id is not None:
		# 		next_user = prenotazioni_in_coda.filter(queue_place=0).get().utente
		# 		PrenotazioneDelete.notify_next_in_line(next_user.email, tavolo_liberato_id, self.object.data_ora)
		#
		# 		prenotazioni_in_coda.filter(queue_place=0).update(tavolo_id=tavolo_liberato_id, queue_place=None)
		# 		prenotazioni_in_coda.filter(queue_place__gt=0).update(queue_place=F('queue_place') - 1)
		# 	elif queue_place_liberato is not None:
		# 		prenotazioni_in_coda.filter(queue_place__gt=queue_place_liberato).update(
		# 			queue_place=F('queue_place') - 1)

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
