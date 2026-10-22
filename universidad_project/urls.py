from django.contrib import admin
from django.urls import path

from gestion import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.inicio, name="inicio"),
    path("health/", views.health, name="health"),
]
