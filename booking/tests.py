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
	lista_tavoli = []
	utente_comodo = None
	utente_staff_comodo = None
	lista_utenti = []
	data_giusta_comoda = timezone.now().date() + timedelta(days=1)

	def setUp(self):
		self.utente_staff_comodo = User.objects.create(username="TestStaff", email="test@test.com", is_staff=True)
		self.utente_comodo = User.objects.create(username="TestPlebeian", email="test@test.com")

		self.tavolo_comodo = Tavolo.objects.create(nome="A1", abilitato=True)
		Tavolo.objects.create(nome="A2", abilitato=True)
		Tavolo.objects.create(nome="A3", abilitato=False)
		# self.utente_staff_comodo = User.objects.create(username="Staff", email="test1@test.com", is_staff=True)
		# self.utente_comodo = User.objects.create(username="Giovanni", email="test2@test.com")
		# self.lista_utenti.append(self.utente_staff_comodo)
		# self.lista_utenti.append(self.utente_comodo)
		# self.lista_utenti.append(User.objects.create(username="Mario", email="test3@test.com"))
		# self.lista_utenti.append(User.objects.create(username="Giancarlo", email="test4@test.com"))
		# self.lista_utenti.append(User.objects.create(username="Pietro", email="test5@test.com"))
		# self.lista_utenti.append(User.objects.create(username="Pompelmo", email="test6@test.com"))
		# self.lista_utenti.append(User.objects.create(username="Cavallo", email="test7@test.com"))
		#
		# self.tavolo_comodo = Tavolo.objects.create(nome="A1", abilitato=True)
		# self.lista_tavoli.append(self.tavolo_comodo)
		# self.lista_tavoli.append(Tavolo.objects.create(nome="A2", abilitato=True))
		# self.lista_tavoli.append(Tavolo.objects.create(nome="A4", abilitato=True))
		# self.lista_tavoli.append(Tavolo.objects.create(nome="A5", abilitato=True))
		# self.lista_tavoli.append(Tavolo.objects.create(nome="A6", abilitato=True))
		# self.lista_tavoli.append(Tavolo.objects.create(nome="A7", abilitato=False))
		# self.lista_tavoli.append(Tavolo.objects.create(nome="A8", abilitato=False))

	# def tearDown(self) -> None:
	# 	self.lista_utenti = []
	# 	self.lista_tavoli = []
		# User.objects.all().delete()
		# Tavolo.objects.all().delete()
		# Prenotazione.objects.all().delete()

	def test_save_booking_in_the_past(self):
		time = timezone.now().date()
		kwargs = {'data_ora': time, 'tavolo': self.tavolo_comodo, 'utente': self.utente_comodo}
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)
		time = timezone.now().date() - timedelta(days=1)
		kwargs['data_ora'] = time
		self.assertRaisesMessage(ValidationError, "passato",
								 Prenotazione.objects.create, **kwargs)

	def test_save_booking_enqueue_in_the_past(self):
		time = timezone.now().date()
		kwargs = {'data_ora': time, 'utente': self.utente_comodo, 'queue_place': 0}
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)
		time = timezone.now().date() - timedelta(days=1)
		kwargs['data_ora'] = time
		self.assertRaisesMessage(ValidationError, "passato",
								 Prenotazione.objects.create, **kwargs)

	def test_save_booking(self):
		time = self.data_giusta_comoda
		preno = Prenotazione.objects.create(data_ora=time, tavolo=self.tavolo_comodo, utente=self.utente_comodo)
		self.assertIsNotNone(preno)
		self.assertIsInstance(preno, Prenotazione)

	def test_save_booking_enqueue(self):
		time = self.data_giusta_comoda
		preno = Prenotazione.objects.create(data_ora=time, utente=self.utente_comodo, queue_place=0)
		self.assertIsNotNone(preno)
		self.assertIsInstance(preno, Prenotazione)

	def test_save_booking_same_tavolo_same_time(self):
		time = self.data_giusta_comoda
		preno = Prenotazione.objects.create(data_ora=time, tavolo=self.tavolo_comodo, utente=self.utente_comodo)
		self.assertIsNotNone(preno)
		self.assertIsInstance(preno, Prenotazione)

		kwargs = {'data_ora': time, 'tavolo': self.tavolo_comodo, 'utente': self.utente_staff_comodo}
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)

	def test_save_enqueue_same_time_same_place(self):
		time = self.data_giusta_comoda
		preno = Prenotazione.objects.create(data_ora=time, utente=self.utente_comodo, queue_place=0)
		self.assertIsNotNone(preno)
		self.assertIsInstance(preno, Prenotazione)

		kwargs = {'data_ora': time, 'utente': self.utente_staff_comodo, 'queue_place': 0}
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)

	def test_save_booking_same_user_same_time(self):
		time = self.data_giusta_comoda
		preno = Prenotazione.objects.create(data_ora=time, tavolo=self.tavolo_comodo, utente=self.utente_comodo)
		self.assertIsNotNone(preno)
		self.assertIsInstance(preno, Prenotazione)

		kwargs = {'data_ora': time, 'tavolo': self.tavolo_comodo, 'utente': self.utente_comodo}
		self.assertRaisesMessage(ValidationError, "",
								 Prenotazione.objects.create, **kwargs)

	# def test_save_many_bookings_many_enqueued(self):
	# 	time = self.data_giusta_comoda
	# 	tavoli_abilitati = [t for t in self.lista_tavoli if t.abilitato]
	# 	for tavolo, utente in tavoli_abilitati, self.lista_utenti[:len(tavoli_abilitati)]:
	# 		preno = Prenotazione.objects.create(data_ora=time, tavolo=tavolo, utente=utente)
	# 		self.assertIsNotNone(preno)
	# 		self.assertIsInstance(preno, Prenotazione)
	#
	# 	i = 0
	# 	for utente in self.lista_utenti[len(tavoli_abilitati):]:
	# 		preno = Prenotazione.objects.create(data_ora=time, utente=self.utente_comodo, queue_place=i)
	# 		self.assertIsNotNone(preno)
	# 		self.assertIsInstance(preno, Prenotazione)
	# 		i += 1


class DashboardViewTests(TestCase):
	def test_qualcosaltro(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': '2021',
												   'month': '09',
										   			'day': '12'}))
		self.assertEqual(response.status_code, 200)
