from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsTemplateView, ProductDetailView, ProductListView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
