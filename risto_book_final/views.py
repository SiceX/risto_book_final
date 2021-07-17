import logging
from django.http import HttpResponse


_logger = logging.getLogger(__name__)


def maintenance(request):
    _logger.debug(request)
    return HttpResponse("Sito in manutenzione")
