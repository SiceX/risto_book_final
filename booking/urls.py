from django.urls import path
from booking.views import TavoloDetail, TavoloList, TavoloCreate, DashboardPrenotazioni

app_name = 'booking'

urlpatterns = [
	path('tavoli/<str:pk>/detail', TavoloDetail.as_view(), name='tavolo-detail'),
	path('tavoli/create', TavoloCreate.as_view(), name='tavolo-create'),
	# path('tavoli/updateList', TavoloAbilitateList.as_view(), name='tavolo-create'),
	path('tavoli/list', TavoloList.as_view(), name='tavolo-list'),
	path('prenotazioni/dashboard/<int:year>/<int:month>/<int:day>', DashboardPrenotazioni.as_view(),
		name='dashboard-prenotazioni')
]
