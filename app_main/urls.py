from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("invoices/", views.invoices, name="invoices"),
    path("suppliers/", views.suppliers, name="suppliers"),
    path("<uuid:id>/", views.detail, name="detail"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
]
