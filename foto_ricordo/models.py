from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def upload_to(instance, filename):
	return 'foto_ricordo/%s-%s' % (timezone.now().strftime("%Y%m%d-%H%M%S"), filename)


class FotoRicordo(models.Model):
	foto_ricordo = models.ImageField(upload_to=upload_to, null=False)
	data = models.DateTimeField(null=False)

	class Meta:
		verbose_name_plural = 'Foto Ricordo'

	def __str__(self):
		return f'{self.data} - {self.pk}'
