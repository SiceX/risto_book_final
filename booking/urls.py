from django.urls import path
from booking.views import TavoloDetail, TavoloList

app_name = 'booking'


urlpatterns = [
	path('tavoli/<int:pk>/detail', TavoloDetail.as_view(), name='tavolo-detail'),
	path('tavoli/list', TavoloList.as_view(), name='tavolo-list')
]
