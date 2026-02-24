from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    preview_image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="Превью-изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")


def __str__(self):
    return self.title


class Meta:
    verbose_name = "Запись блога"
    verbose_name_plural = "Записи блога"
