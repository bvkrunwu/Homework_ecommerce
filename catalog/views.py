from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView

from .models import Product


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = self.model.objects.order_by("-created_at")[:5]
        context["latest_products"] = latest_products
        for product in latest_products:
            print(f"Последний продукт: {product.name}, Дата создания: {product.created_at}")
        return context


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        response_message = f'Привет {name}! Ваш номер: {phone}.  Сообщение: " {message} " получено.'
        return HttpResponse(response_message)


class ProductDetailView(DetailView):
    model = Product
