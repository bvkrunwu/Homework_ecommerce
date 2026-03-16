from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаём группу и назначаем права"

    def handle(self, *args, **options):
        groups = {
            "Модератор продуктов": [
                "can_unpublish_product",
                "can_delete_product",
            ]
        }

        try:
            content_type = ContentType.objects.get(app_label="catalog", model="product")
        except ContentType.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    "Контент‑тип catalog.product не найден."
                    "Убедитесь, что приложение catalog и модель Product существуют."
                )
            )
            return

        for group_name, perm_codenames in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Создана группа: {group_name}"))
            else:
                self.stdout.write(f"Группа уже существует: {group_name}")

            for codename in perm_codenames:
                try:
                    permission = Permission.objects.get(codename=codename, content_type=content_type)
                    group.permissions.add(permission)
                    self.stdout.write(f"Добавлено право: {codename}")
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Право не найдено: {codename}"))

        self.stdout.write(self.style.SUCCESS("Процесс создания группы и назначения прав завершён!"))
