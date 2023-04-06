from django.urls import path

from . import views

app_name = "grocery"
urlpatterns = [
    # path("", views.index, name="index"),
    path("<int:storage_id>/", views.detail, name="detail"),
    # path("<int:storage_id>/store", views.store, name="store"),

    path("", views.IndexView.as_view(), name="index"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:storage_id>/store", views.store, name="store"),
    path("<int:storage_id>/ticket", views.ticket, name="ticket"),
    path("<int:storage_id>/upload", views.upload, name="upload"),
]