import logging
from django.http import HttpResponse
from django.views.generic import TemplateView

_logger = logging.getLogger(__name__)


def maintenance(request):
    _logger.debug(request)
    return HttpResponse("Sito in manutenzione")


class Home(TemplateView):
    template_name = 'home.html'
