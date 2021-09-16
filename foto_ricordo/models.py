from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def upload_to(instance, filename):
	return 'foto_ricordo/%s-%s' % (timezone.now().strftime("%Y%m%d"), filename)


class FotoRicordo(models.Model):
	foto_ricordo = models.ImageField(upload_to=upload_to, null=False)
	data_ora = models.DateTimeField(null=False)

	class Meta:
		verbose_name_plural = 'Foto Ricordo'

	def __str__(self):
		return f'{self.data_ora} - {self.pk}'
