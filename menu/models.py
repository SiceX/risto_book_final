from django.db import models


class Piatto(models.Model):
	nome = models.CharField(max_length=50)
	descrizione = models.CharField(max_length=500)

	class Meta:
		verbose_name_plural = 'Piatti'

	def __str__(self):
		return f'{self.nome} - {self.pk}'
