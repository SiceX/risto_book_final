from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def upload_to(instance, filename):
	return 'user/%s/%s' % (instance.user_id, filename)


class ImmagineProfilo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(upload_to=upload_to)

	class Meta:
		unique_together = [['user', 'profile_picture']]
		verbose_name_plural = 'Immagini Profilo'

	def __str__(self):
		return f'{self.user} - {self.pk}'
