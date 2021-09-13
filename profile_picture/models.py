from django.conf import settings
from django.db import models


class ImmagineProfilo(models.Model):
	utente = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)
	immagine = models.ImageField()

	class Meta:
		unique_together = [['id', 'utente']]
		verbose_name_plural = 'Immagini Profilo'

	def __str__(self):
		return f'{self.utente} - {self.pk}'
