from django.utils import timezone

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, ListView

from foto_ricordo.forms import CreateFotoRicordoForm
from foto_ricordo.models import FotoRicordo


class FotoRicordoListView(ListView):
    model = FotoRicordo
    template_name = 'foto_ricordo/list.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(utente=self.request.user,  data_ora__gte=timezone.now())


def FotoRicordoCreateView(request):
    if request.method == 'POST':
        form = CreateFotoRicordoForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/home')
    else:
        form = CreateFotoRicordoForm()
    return render(request, 'foto_ricordo/create_foto_ricordo.html', {'form': form})
