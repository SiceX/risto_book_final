from django.db import models


STATO_TAVOLO_CHOICES = [
	# ('L', 'Libero'),
	# ('P', 'Prenotato'),
	('A', 'Abilitato'),
	('D', 'Disabilitato')
]


class Tavolo(models.Model):
	nome = models.CharField(max_length=5, primary_key=True)
	stato = models.CharField(max_length=1, choices=STATO_TAVOLO_CHOICES, default='A')

	class Meta:
		verbose_name_plural = 'Tavoli'

	def get_display_stato(self):
		state = [tupla for tupla in STATO_TAVOLO_CHOICES if tupla[0] == self.stato][0]
		return state[1]

	def __str__(self):
		return f'{self.nome} - {self.get_display_stato()} - {self.pk}'


class Prenotazione(models.Model):
	data_ora = models.DateTimeField()
	tavolo = models.ForeignKey(
		'Tavolo',
		on_delete=models.CASCADE
	)
	# utente
