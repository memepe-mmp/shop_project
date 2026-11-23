from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.product_create, name="create"),
    path("<int:pk>/", views.product_detail, name="detail"),
    path("<int:pk>/edit/", views.product_update, name="update"),
    path("<int:pk>/delete/", views.product_delete, name="delete"),
]