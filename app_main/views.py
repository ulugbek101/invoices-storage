from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Supplier


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def suppliers(request):
    all_suppliers = Supplier.objects.all()
    page = request.GET.get('page', 1)
    context = {}

    if request.method == 'POST':
        query = request.POST.get('product_id', '').strip()

        if query:
            filtered_suppliers = Supplier.objects.filter(
                Q(sender__icontains=query) |
                Q(country__icontains=query) |
                Q(weight__icontains=query)
            )
            context.update({"id": query})
        else:
            filtered_suppliers = all_suppliers  # If query is empty, return all

        paginator = Paginator(filtered_suppliers, 50)  # Apply pagination to filtered results
    else:
        paginator = Paginator(all_suppliers, 50)

    try:
        qs = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        qs = paginator.page(1)

    context.update({
        "error": not qs.object_list.exists(),
        "message": "Поставщики не найдены" if not qs.object_list.exists() else "Поставщики найдены",
        "all_suppliers": qs,
    })

    return render(request, 'suppliers.html', context)


@login_required(login_url="login")
def invoices(request):
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
        return render(request, "invoices.html", context)

    from_product = request.GET.get("from")

    if from_product:
        try:
            products = Product.objects.filter(invoice=from_product)
        except:
            products = None
        context = {"success": True, "products": products, "id": from_product}
    else:
        context = {}
    return render(request, "invoices.html", context)


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
