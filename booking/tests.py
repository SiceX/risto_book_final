from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Prenotazione, Tavolo


# noinspection DuplicatedCode
class PrenotazioneTests(TestCase):

	tavolo_comodo = None
	utente_comodo = None
	utente_staff_comodo = None
	data_giusta_comoda = timezone.now().date() + timedelta(days=1)

	def setUp(self):
		self.utente_staff_comodo = User.objects.create(username="TestStaff", email="test@test.com", is_staff=True)
		self.utente_comodo = User.objects.create(username="TestPlebeian", email="test@test.com")

		self.tavolo_comodo = Tavolo.objects.create(nome="A1", abilitato=True)
		Tavolo.objects.create(nome="A2", abilitato=True)
		Tavolo.objects.create(nome="A3", abilitato=False)

	def test_save_booking_in_the_past(self):
		time = timezone.now().date()
		kwargs = {'data_ora': time, 'tavolo': self.tavolo_comodo, 'utente': self.utente_comodo}
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)
		time = timezone.now().date() - timedelta(days=1)
		kwargs['data_ora'] = time
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)

	def test_save_booking(self):
		time = self.data_giusta_comoda
		preno = Prenotazione.objects.create(data_ora=time, tavolo=self.tavolo_comodo, utente=self.utente_comodo)
		self.assertIsNotNone(preno)
		self.assertIsInstance(preno, Prenotazione)

	def test_save_booking_same_tavolo_same_time(self):
		time = self.data_giusta_comoda
		preno = Prenotazione.objects.create(data_ora=time, tavolo=self.tavolo_comodo, utente=self.utente_comodo)
		self.assertIsNotNone(preno)
		self.assertIsInstance(preno, Prenotazione)

		kwargs = {'data_ora': time, 'tavolo': self.tavolo_comodo, 'utente': self.utente_staff_comodo}
		self.assertRaisesMessage(IntegrityError, "",
								 Prenotazione.objects.create, **kwargs)

	def test_save_booking_enqueue_in_the_past(self):
		time = timezone.now().date()
		kwargs = {'data_ora': time, 'utente': self.utente_comodo, 'queue_place': 0}
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)
		time = timezone.now().date() - timedelta(days=1)
		kwargs['data_ora'] = time
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)

	def test_save_booking_enqueue(self):
		time = self.data_giusta_comoda
		preno = Prenotazione.objects.create(data_ora=time, utente=self.utente_comodo, queue_place=0)
		self.assertIsNotNone(preno)
		self.assertIsInstance(preno, Prenotazione)


class DashboardViewTests(TestCase):
	def test_qualcosaltro(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': '2021',
												   'month': '09',
										   			'day': '12'}))
		self.assertEqual(response.status_code, 200)
