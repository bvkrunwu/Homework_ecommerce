from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Product


def home(request):
    latest_products = Product.objects.order_by("-created_at")[:5]
    for product in latest_products:
        print(f"Последний продукт: {product.name}, Дата создания: {product.created_at}")
    all_products = Product.objects.all()
    context = {"latest_products": latest_products, "products": all_products}
    return render(request, "catalog/home.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f'Привет {name}! Ваш номер: {phone}.  Сообщение: " {message} " получено.')
    return render(request, "catalog/contacts.html")


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)
