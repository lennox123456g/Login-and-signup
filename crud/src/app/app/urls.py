from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/email-signup/', include('appsot.urls')), #email fro Active campaign urls
    path('admin/', admin.site.urls),
]

