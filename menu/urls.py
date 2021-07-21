from django.urls import path
from menu.views import PiattoList

app_name = 'menu'


urlpatterns = [
	path('piatti', PiattoList.as_view(), name='menu')
]
