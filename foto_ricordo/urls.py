from django.urls import path
from foto_ricordo.views import FotoRicordoListView, foto_ricordo_create_view

app_name = 'foto_ricordo'

urlpatterns = [
	path('foto_ricordo/list', FotoRicordoListView.as_view(), name='foto-ricordo-list'),
	path('foto_ricordo/upload', foto_ricordo_create_view, name='foto-ricordo-create')
]
