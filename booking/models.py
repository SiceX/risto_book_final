import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Tavolo(models.Model):
	nome = models.CharField(max_length=5, primary_key=True)
	abilitato = models.BooleanField(verbose_name='Abilitato', default=True, null=False)

	class Meta:
		verbose_name_plural = 'Tavoli'

	def __str__(self):
		return f'{self.nome}'
		# return f'{self.nome} - {self.abilitato} - {self.pk}'


class Prenotazione(models.Model):
	data_ora = models.DateTimeField()
	tavolo = models.ForeignKey(
		'Tavolo',
		on_delete=models.CASCADE,
		null=True
	)
	utente = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)
	queue_place = models.PositiveSmallIntegerField(
		validators=[MinValueValidator(0)],
		null=True
	)

	class Meta:
		unique_together = [['data_ora', 'queue_place'],
						   ['data_ora', 'utente']]
		verbose_name_plural = 'Prenotazioni'

	def save(self, *args, **kwargs):
		if self.data_ora.date() < (timezone.now().date() + datetime.timedelta(days=1)):
			raise ValidationError("Non è possibile prenotare pranzi o cene per oggi o nel passato")
		super(Prenotazione, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.tavolo} - {self.data_ora} - {self.pk}'
