from django.core.exceptions import ValidationError
from django.forms import ModelForm

from catalog.models import Product

FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data["name"]
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise ValidationError("Название содержит запрещённое слово")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise ValidationError("Описание содержит запрещённое слово")
        return description

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data["purchase_price"]
        if purchase_price is not None and purchase_price <= 0:
            raise ValidationError("Цена не может быть отрицательной")
        return purchase_price
