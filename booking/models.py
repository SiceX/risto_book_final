from django.db import models


# Create your models here.


STATO_TAVOLO_CHOICES = [
	('L', 'Libero'),
	('P', 'Prenotato'),
	('D', 'Disabilitato')
]


class Tavolo(models.Model):
	stato = models.CharField(max_length=1, choices=STATO_TAVOLO_CHOICES)
	nome = models.CharField(max_length=5)

	class Meta:
		verbose_name_plural = 'Tavoli'

	def __str__(self):
		state = [tupla for tupla in STATO_TAVOLO_CHOICES if tupla[0] == self.stato][0]
		return f'{self.nome} - {state[1]}'


class Prenotazione(models.Model):
	data_ora = models.DateTimeField()
	tavolo = models.ForeignKey(
		'Tavolo',
		on_delete=models.CASCADE
	)
	# utente
