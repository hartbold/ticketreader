from django.urls import path

from . import views

app_name = "grocery"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:storage_id>/", views.detail, name="detail"),
    path("<int:storage_id>/store", views.store, name="store"),
]