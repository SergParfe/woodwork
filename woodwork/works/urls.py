from django.urls import path

from works.views import index

app_name = 'works'

urlpatterns = [
    path('', index, name='index'),
    # path('ice_cream/', views.ice_cream_list),
    # path('ice_cream/<int:pk>/', views.ice_cream_detail),
]
