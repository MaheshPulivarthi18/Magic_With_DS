# example/urls.py
from django.urls import path
from . import views
import os

urlpatterns = [
    path("", views.home),
    path("visualize/", views.visualize, name="visualize"),
]
