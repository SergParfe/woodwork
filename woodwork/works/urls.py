from django.urls import include, path

# from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet
from works.views import index

app_name = 'works'

urlpatterns = [
    path('', index),
    # path('ice_cream/', views.ice_cream_list),
    # path('ice_cream/<int:pk>/', views.ice_cream_detail),
]
