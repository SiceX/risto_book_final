from django.urls import path

from admin_tools.views import TavoloDetail, TavoloCreate, TavoloList, TavoloListAndUpdate, TavoloDelete

app_name = 'admin_tools'

urlpatterns = [
	path('tavoli/<str:pk>/detail', TavoloDetail.as_view(), name='tavolo-detail'),
	path('tavoli/<str:pk>/delete', TavoloDelete.as_view(), name='tavolo-delete'),
	path('tavoli/create', TavoloCreate.as_view(), name='tavolo-create'),
	path('tavoli/manage-tavoli', TavoloListAndUpdate.as_view(), name='tavolo-manage-list'),
	path('tavoli/list', TavoloList.as_view(), name='tavolo-list'),
]