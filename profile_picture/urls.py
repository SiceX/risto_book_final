from django.urls import path
from menu.views import PiattoList
from profile_picture.views import upload_file

app_name = 'profile_picture'


urlpatterns = [
	path('propic', upload_file, name='edit_propic')
]
