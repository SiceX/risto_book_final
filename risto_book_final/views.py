import logging

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from risto_book_final.forms import UserCreationWithEmailForm, EditProfileForm

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


class UserEditView(UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    # def get_initial(self):
    #     user_id = self.request.user.id
    #
    #     return super().get_initial()

    def get_object(self, queryset=None):
        return self.request.user
