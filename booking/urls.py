from django.urls import path
from booking.views import TavoloDetail, TavoloList, TavoloCreate, DashboardPrenotazioni, PrenotazioneCreate, \
	PrenotazioneList, PrenotazioneDelete, FindFirstFreeDayRedirectView

app_name = 'booking'

urlpatterns = [
	path('tavoli/<str:pk>/detail', TavoloDetail.as_view(), name='tavolo-detail'),
	path('tavoli/create', TavoloCreate.as_view(), name='tavolo-create'),
	# path('tavoli/updateList', TavoloAbilitateList.as_view(), name='tavolo-create'),
	path('tavoli/list', TavoloList.as_view(), name='tavolo-list'),
	path('prenotazioni/list', PrenotazioneList.as_view(), name='prenotazione-list'),
	path('prenotazioni/<str:pk>/delete', PrenotazioneDelete.as_view(), name='prenotazione-delete'),
	path('prenotazioni/dashboard/<int:year>/<int:month>/<int:day>', DashboardPrenotazioni.as_view(),
		name='dashboard-prenotazioni'),
	path('prenotazioni/dashboard/find-free', FindFirstFreeDayRedirectView.as_view(),
		name='dashboard-prenotazioni-find'),
	path('prenotazioni/prenota/<str:tavolo>/<int:year>/<int:month>/<int:day>/<int:hour>',
		 PrenotazioneCreate.as_view(), name='prenota-tavolo'),
	path('prenotazioni/prenota/<int:year>/<int:month>/<int:day>/<int:hour>',
		 PrenotazioneCreate.as_view(), name='prenota-tavolo-in-coda')
]
