from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import include, path
from works.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('works/', include('works.urls')),
    path('', index),
]

admin.site.unregister(Group)  # disable Groups in admin panel
