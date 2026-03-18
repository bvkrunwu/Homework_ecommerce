from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    """Получает данные по продуктам из кэша, если кэш пуст, получаем данные из БД"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products, timeout=300)
    return products


def get_products_by_category_from_cache(category_id):
    """Получает продукты указанной категории из кэша, если кэш пуст, получаем данные из БД"""
    if not CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, is_published=True).select_related("category")
    key = f"products_by_category_{category_id}"
    products = cache.get(key)
    if products is not None:
        return products
    products = (
        Product.objects.filter(category_id=category_id, is_published=True)
        .select_related("category")
        .order_by("-created_at")
    )
    cache.set(key, products, timeout=300)
    return products
