from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from foto_ricordo.forms import CreateFotoRicordoForm
from foto_ricordo.models import FotoRicordo


class FotoRicordoListView(ListView):
    model = FotoRicordo
    template_name = 'foto_ricordo/list.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(utente=self.request.user,  data_ora__gte=timezone.now())


def foto_ricordo_create_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateFotoRicordoForm(request.POST, request.FILES)
            if form.is_valid():
                # file is saved
                form.save()
                return HttpResponseRedirect('/foto_ricordo/foto_ricordo/list')
        else:
            form = CreateFotoRicordoForm()
        return render(request, 'foto_ricordo/create_foto_ricordo.html', {'form': form})
    else:
        return HttpResponseRedirect('/home')
