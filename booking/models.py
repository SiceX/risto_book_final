from django.conf import settings
from django.db import models


class Tavolo(models.Model):
	nome = models.CharField(max_length=5, primary_key=True)
	abilitato = models.BooleanField(verbose_name='Abilitato', default=True, null=False)
		# models.CharField(max_length=1, choices=STATO_TAVOLO_CHOICES, default='A')

	class Meta:
		verbose_name_plural = 'Tavoli'

	def __str__(self):
		return f'{self.nome} - {self.abilitato} - {self.pk}'


class Prenotazione(models.Model):
	data_ora = models.DateTimeField()
	tavolo = models.ForeignKey(
		'Tavolo',
		on_delete=models.CASCADE
	)
	utente = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)

	class Meta:
		unique_together = ['data_ora', 'tavolo', 'utente']
		verbose_name_plural = 'Prenotazioni'

	def __str__(self):
		return f'{self.tavolo} - {self.data_ora} - {self.pk}'
