import logging

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from risto_book_final.forms import UserCreationWithEmailForm

_logger = logging.getLogger(__name__)


def maintenance(request):
    _logger.debug(request)
    return HttpResponse("Sito in manutenzione")


class Home(TemplateView):
    template_name = 'home.html'


class UserCreationView(CreateView):
    form_class = UserCreationWithEmailForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('home')
