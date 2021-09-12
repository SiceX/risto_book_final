from django.test import TestCase
from django.urls import reverse

from .models import Prenotazione


class PrenotazioneTests(TestCase):
	def test_qualcosa(self):
		self.assertTrue(True)


class DashboardViewTests(TestCase):
	def test_qualcosaltro(self):
		response = self.client.get(reverse('booking:dashboard-prenotazioni',
										   kwargs={'year': '2021',
												   'month': '09',
										   			'day': '12'}))
		self.assertEqual(response.status_code, 200)
