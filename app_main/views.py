from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


@login_required(login_url="login")
def index(request):
    context = {}
    return render(request, "index.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")


class UserLogin(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("index")
    redirect_authenticated_user = reverse_lazy("index")
