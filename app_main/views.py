from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Product


@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        try:
            products = Product.objects.filter(invoice=product_id)
        except:
            products = None

        if not products:
            context = {"success": False, "products": None, "product_id": product_id}
        else:
            context = {"success": True, "products": products, "product_id": product_id}
        return render(request, "index.html", context)

    context = {}
    return render(request, "index.html", context)


@login_required(login_url="login")
def detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    context = {
        "product": product,
    }
    return render(request, "detail.html", context)

def user_logout(request):
    logout(request)
    return redirect("login")


class UserLogin(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("index")
    redirect_authenticated_user = reverse_lazy("index")
