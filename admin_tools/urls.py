from django.urls import path

from admin_tools.views import TavoloDetail, TavoloCreate, TavoloList

app_name = 'admin_tools'

urlpatterns = [
	path('tavoli/<str:pk>/detail', TavoloDetail.as_view(), name='tavolo-detail'),
	path('tavoli/create', TavoloCreate.as_view(), name='tavolo-create'),
	# path('tavoli/updateList', TavoloAbilitateList.as_view(), name='tavolo-create'),
	path('tavoli/list', TavoloList.as_view(), name='tavolo-list'),
]