from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Document


@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        document_id = request.POST.get("document_id")

        try:
            document = Document.objects.get(id=document_id)
        except:
            document = None

        if not document:
            context = {"success": False, "document": None, "document_id": document_id}
        else:
            context = {"success": True, "document": document, "document_id": document_id}
        return render(request, "index.html", context)

    context = {}
    return render(request, "index.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")


class UserLogin(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("index")
    redirect_authenticated_user = reverse_lazy("index")
