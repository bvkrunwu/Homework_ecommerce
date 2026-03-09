from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import BooleanField, ClearableFileInput, ModelForm
from django.utils.deconstruct import deconstructible

from catalog.models import Product


@deconstructible
class ContentTypeRestrictedFileValidator:
    def __init__(self, content_types=None, max_upload_size=None):
        self.content_types = content_types or []
        self.max_upload_size = max_upload_size

    def __call__(self, data):
        if hasattr(data, "content_type"):
            content_type = data.content_type.lower()
            if content_type not in self.content_types:
                raise ValidationError(
                    f"Файл имеет неверный формат. Поддерживаются только {', '.join(self.content_types)}."
                )

            if self.max_upload_size and data.size > self.max_upload_size:
                size_in_mb = round(self.max_upload_size / (1024 * 1024), 2)
                raise ValidationError(f"Размер файла превышает максимальное разрешенное значение {size_in_mb} МБ.")


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "image": ClearableFileInput(attrs={"accept": "image/jpeg,image/png"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validator = ContentTypeRestrictedFileValidator(
            content_types=["image/jpeg", "image/png"], max_upload_size=5 * 1024 * 1024
        )
        self.fields["image"].validators.append(validator)

    def clean_name(self):
        name = self.cleaned_data["name"]
        forbidden_words = settings.FORBIDDEN_WORDS
        for word in forbidden_words:
            if word.lower() in name.lower():
                raise ValidationError(f"Название содержит запрещённое слово '{word}'.")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        forbidden_words = settings.FORBIDDEN_WORDS
        for word in forbidden_words:
            if word.lower() in description.lower():
                raise ValidationError(f"Описание содержит запрещённое слово '{word}'.")
        return description

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data["purchase_price"]
        if purchase_price is not None and purchase_price < 0:
            raise ValidationError(f"Цена не может быть отрицательной '{purchase_price}'.")
        return purchase_price
