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
            context = {"success": False, "products": None, "id": product_id}
        else:
            context = {"success": True, "products": products, "id": product_id}
        return render(request, "index.html", context)

    from_product = request.GET.get("from")

    if from_product:
        try:
            products = Product.objects.filter(invoice=from_product)
        except:
            products = None

    context = {"success": True, "products": products, "id": from_product}
    return render(request, "index.html", context)


@login_required(login_url="login")
def detail(request, id):
    product = get_object_or_404(Product, id=id)
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
