from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = self.model.objects.order_by("-created_at")[:5]
        context["latest_products"] = latest_products
        for product in latest_products:
            print(f"Последний продукт: {product.name}, Дата создания: {product.created_at}")
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        user = self.request.user

        # Проверяем: владелец ИЛИ имеет право на редактирование ИЛИ на удаление
        can_edit_delete = (
            product.owner == user
            or user.has_perm("catalog.can_unpublish_product")
            or user.has_perm("catalog.can_delete_product")
        )

        context["can_edit_delete"] = can_edit_delete
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if (
            product.owner != request.user
            and not request.user.has_perm("catalog.can_unpublish_product")
            and not request.user.has_perm("catalog.can_delete_product")
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        return ProductForm


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user

        # Разрешаем удаление: владельцу ИЛИ пользователю с правом can_delete_product ИЛИ can_unpublish_product
        if (
            product.owner != user
            and not user.has_perm("catalog.can_delete_product")
            and not user.has_perm("catalog.can_unpublish_product")
        ):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class ContactsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        response_message = f'Привет {name}! Ваш номер: {phone}.  Сообщение: " {message} " получено.'
        return HttpResponse(response_message)
