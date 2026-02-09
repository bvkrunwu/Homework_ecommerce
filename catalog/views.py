from django.http import HttpResponse
from django.shortcuts import render
from .models import Product


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for product in latest_products:
        print(f'Последний продукт: {product.name}, Дата создания: {product.created_at}')
    return render(request, 'home.html', {'latest_products': latest_products})


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Привет {name}! Ваш номер: {phone}.  Сообщение: " {message} " получено.')
    return render(request, 'contacts.html')
