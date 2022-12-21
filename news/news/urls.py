from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  #дописал 20.12.
    path('admin/', admin.site.urls),
    path('', include ('newspaper.urls')),
    path('members/', include ('django.contrib.auth.urls')),
    path('members/', include ('members.urls')),
]
