from django.urls import path
from booking.views import DashboardPrenotazioni, PrenotazioneCreate, \
	PrenotazioneList, PrenotazioneDelete, FindFirstFreeDayRedirectView, FindFirstFreeDayForTableRedirectView, \
	dashboardPrenotazioniController

app_name = 'booking'

urlpatterns = [
	path('prenotazioni/list', PrenotazioneList.as_view(), name='prenotazione-list'),
	path('prenotazioni/<str:pk>/delete', PrenotazioneDelete.as_view(), name='prenotazione-delete'),
	path('prenotazioni/dashboard/<int:year>/<int:month>/<int:day>', dashboardPrenotazioniController,
		name='dashboard-prenotazioni'),
	path('prenotazioni/dashboard/find-free', FindFirstFreeDayRedirectView.as_view(),
		name='dashboard-prenotazioni-find'),
	path('prenotazioni/dashboard/find-free/<str:tavolo>', FindFirstFreeDayForTableRedirectView.as_view(),
		name='dashboard-prenotazioni-find-for-table'),
	path('prenotazioni/prenota/<str:tavolo>/<int:year>/<int:month>/<int:day>/<int:hour>',
		 PrenotazioneCreate.as_view(), name='prenota-tavolo'),
	path('prenotazioni/prenota/<int:year>/<int:month>/<int:day>/<int:hour>',
		 PrenotazioneCreate.as_view(), name='prenota-tavolo-in-coda')
]
