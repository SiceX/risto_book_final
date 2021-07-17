from django.urls import path
from booking.views import TavoloDetail


app_name = 'booking'


urlpatterns = [
	path('tavolo/<int:pk>/detail', TavoloDetail.as_view(), name='tavolo-detail')
]
