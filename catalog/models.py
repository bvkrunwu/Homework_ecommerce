from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="Изображение")
    purchase_price = models.IntegerField(verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products", verbose_name="Категория"
    )

    def __str__(self):
        return f"{self.name} ({self.category.name}), Цена покупки: {self.purchase_price} руб."

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
