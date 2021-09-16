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
	data_giusta_comoda = (timezone.now() + timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)

	def setUp(self):
		self.utente_staff_comodo = User.objects.create(username="Staff", email="test1@test.com", is_staff=True)
		self.utente_comodo = User.objects.create(username="Giovanni", email="test2@test.com")
		User.objects.create(username="Mario", email="test3@test.com")
		User.objects.create(username="Giancarlo", email="test4@test.com")
		User.objects.create(username="Pietro", email="test5@test.com")
		User.objects.create(username="Pompelmo", email="test6@test.com")
		User.objects.create(username="Cavallo", email="test7@test.com")

		self.tavolo_comodo = Tavolo.objects.create(nome="A1", abilitato=True)
		Tavolo.objects.create(nome="A2", abilitato=True)
		Tavolo.objects.create(nome="A4", abilitato=True)
		Tavolo.objects.create(nome="A5", abilitato=True)
		Tavolo.objects.create(nome="A6", abilitato=True)
		Tavolo.objects.create(nome="A7", abilitato=False)
		Tavolo.objects.create(nome="A8", abilitato=False)

	def tearDown(self) -> None:
		self.lista_utenti = []
		self.lista_tavoli = []
		User.objects.all().delete()
		Tavolo.objects.all().delete()
		Prenotazione.objects.all().delete()

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

	def test_save_many_bookings_many_enqueued(self):
		time = self.data_giusta_comoda
		tavoli_abilitati = Tavolo.objects.filter(abilitato=True).iterator()
		utenti = User.objects.all().iterator()
		for tavolo, utente in zip(tavoli_abilitati, utenti):
			preno = Prenotazione.objects.create(data_ora=time, tavolo=tavolo, utente=utente)
			self.assertIsNotNone(preno)
			self.assertIsInstance(preno, Prenotazione)

		i = 0
		for utente in utenti:
			preno = Prenotazione.objects.create(data_ora=time, utente=utente, queue_place=i)
			self.assertIsNotNone(preno)
			self.assertIsInstance(preno, Prenotazione)
			i += 1


# noinspection DuplicatedCode
class DashboardViewTests(TestCase):
	tavolo_comodo = None
	secondo_tavolo_comodo = None
	lista_tavoli = []
	utente_comodo = None
	utente_staff_comodo = None
	lista_utenti = []
	data_giusta_comoda = (timezone.now() + timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)

	def setUp(self):
		self.utente_staff_comodo = User.objects.create(username="Staff", email="test1@test.com", is_staff=True)
		self.utente_staff_comodo.set_password('lol')
		self.utente_staff_comodo.save()
		self.utente_comodo = User.objects.create(username="Giovanni", email="test2@test.com")
		self.utente_comodo.set_password('lmao')
		self.utente_comodo.save()
		User.objects.create(username="Mario", email="test3@test.com")
		User.objects.create(username="Giancarlo", email="test4@test.com")
		User.objects.create(username="Pietro", email="test5@test.com")
		User.objects.create(username="Pompelmo", email="test6@test.com")
		User.objects.create(username="Cavallo", email="test7@test.com")

		self.tavolo_comodo = Tavolo.objects.create(nome="A1", abilitato=True)
		self.secondo_tavolo_comodo = Tavolo.objects.create(nome="A2", abilitato=True)
		Tavolo.objects.create(nome="A4", abilitato=False)
		Tavolo.objects.create(nome="A5", abilitato=False)

		Prenotazione.objects.create(data_ora=self.data_giusta_comoda, tavolo=self.tavolo_comodo,
									utente=self.utente_staff_comodo)

	def tearDown(self) -> None:
		self.lista_utenti = []
		self.lista_tavoli = []
		User.objects.all().delete()
		Tavolo.objects.all().delete()
		Prenotazione.objects.all().delete()

	def test_redirect_if_in_the_past(self):
		time = timezone.now().date()
		tomorrow = timezone.now().date() + timedelta(days=1)
		expected_url = f"/booking/prenotazioni/dashboard/{tomorrow.year}/{tomorrow.month}/{tomorrow.day}"
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': time.year,
												   'month': time.month,
										   			'day': time.day}),
								   follow=True)
		self.assertRedirects(response, expected_url)

		time = timezone.now().date() - timedelta(days=1)
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': time.year,
												   'month': time.month,
												   'day': time.day}),
								   follow=True)
		self.assertRedirects(response, expected_url)

	def test_200_if_tomorrow_or_later(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		self.assertEquals(response.status_code, 200)

	def test_no_previous_button_if_tomorrow(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		self.assertNotContains(response, "btn-previous")

	def test_no_book_table_buttons_if_not_authenticated(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		self.assertNotContains(response, "id=\"btn-book-")

	def test_book_table_buttons_if_authenticated(self):
		self.client.login(username='Giovanni', password='lmao')
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		self.assertContains(response, "id=\"btn-book-")

	def test_display_only_enabled_tables(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		for tavolo in Tavolo.objects.filter(abilitato=True):
			self.assertContains(response, f"id=\"row-{tavolo.nome}")
		for tavolo in Tavolo.objects.filter(abilitato=False):
			self.assertNotContains(response, f"id=\"row-{tavolo.nome}")

	def test_display_booked_state(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		for tavolo in Tavolo.objects.filter(abilitato=True):
			if Prenotazione.objects.filter(data_ora=self.data_giusta_comoda, tavolo=tavolo).exists():
				self.assertContains(response, f"<td id=\"cell-stato-{tavolo.nome}\">Prenotato</td>")
			else:
				self.assertContains(response, f"<td id=\"cell-stato-{tavolo.nome}\">Libero</td>")

	def test_display_find_free_day_for_table(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		prenotati_pranzo = response.context_data['prenotati_pranzo']
		for tavolo_name in prenotati_pranzo:
			self.assertContains(response, f"id=\"btn-find-free-{tavolo_name}\"")

	def test_display_user_already_booked_notice(self):
		self.client.login(username='Staff', password='lol')
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		self.assertContains(response, "id=\"user-already-booked-notice\"")

	def test_display_all_booked_notice(self):
		Prenotazione.objects.create(data_ora=self.data_giusta_comoda, tavolo=self.secondo_tavolo_comodo,
									utente=self.utente_comodo)
		self.client.login(username='Giovanni', password='lmao')
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': self.data_giusta_comoda.year,
												   'month': self.data_giusta_comoda.month,
												   'day': self.data_giusta_comoda.day}))
		self.assertContains(response, "id=\"all-booked-notice\"")

