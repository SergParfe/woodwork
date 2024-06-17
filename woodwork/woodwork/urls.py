from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from works.views import about_this_site, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('works/', include('works.urls', namespace='works')),
    path('about_this_site/<str:language>/', about_this_site, name='about'),
    path('<str:language>/', index, name='index_language'),
    path('', index, name='index'),
]

handler404 = 'works.views.page_not_found'
handler500 = 'works.views.server_error_page'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
