from django.urls import path
from foto_ricordo.views import FotoRicordoListView, FotoRicordoCreateView

app_name = 'foto_ricordo'

urlpatterns = [
	path('foto_ricordo/list', FotoRicordoListView.as_view(), name='foto-ricordo-list'),
	path('foto_ricordo/upload', FotoRicordoCreateView, name='foto-ricordo-create')
]
