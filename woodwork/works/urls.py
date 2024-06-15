from django.urls import path

from works.views import work_detail, work_list

app_name = 'works'

urlpatterns = [
    path('<slug:slug>/<str:language>/', work_detail, name='work_detail'),
    path('<str:language>/', work_list, name='works_list'),
]
