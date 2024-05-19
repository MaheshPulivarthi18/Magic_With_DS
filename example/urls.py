# example/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path("", views.home),
    path("visualize/", views.visualize, name="visualize"),
    path("favicon.ico", views.favicon),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
