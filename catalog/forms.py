from django import forms
from django.forms import BooleanField

from .models import Product


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        """Инициализация формы с добавлением CSS-классов Bootstrap"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Проверяем, что поле имеет widget и attrs
            if hasattr(field, "widget") and hasattr(field.widget, "attrs"):
                if isinstance(field, BooleanField):
                    field.widget.attrs["class"] = "form-check-input"
                else:
                    field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price", "is_published"]

    def __init__(self, *args, **kwargs):
        """Дополнительная настройка полей формы"""
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите название продукта",  # Текст подсказки внутри поля
            }
        )

        # Настройка атрибутов виджета для поля 'last_name'
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите описание",  # Текст подсказки внутри поля
            }
        )

        # Настройка атрибутов виджета для поля 'email'
        self.fields["price"].widget.attrs.update(
            {
                "class": "form-control",  # Добавление CSS-класса для стилизации поля
                "placeholder": "Введите цену",  # Текст подсказки внутри поля
            }
        )
        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",
                "accept": "image/*",
            }
        )
        if "is_published" in self.fields:
            self.fields["is_published"].widget.attrs.update(
                {
                    "class": "form-check-input",
                }
            )
            self.fields["is_published"].label = "Опубликовано"
            self.fields["is_published"].help_text = (
                "Отметьте, чтобы опубликовать продукт"
            )

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data.get("name")
        if name:
            name_lower = name.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in name_lower:
                    raise forms.ValidationError(
                        f'Название содержит запрещенное слово: "{word}"'
                    )
        return name

    def clean_description(self):
        """Валидация описания продукта"""
        description = self.cleaned_data.get("description")
        if description:
            description_lower = description.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in description_lower:
                    raise forms.ValidationError(
                        f'Описание содержит запрещенное слово: "{word}"'
                    )
        return description

    def clean_price(self):
        """Валидация цены продукта"""
        price = self.cleaned_data.get("price")

        # Проверка, что цена не отрицательная
        if price is not None and price < 0:
            raise forms.ValidationError(
                "Цена не может быть отрицательной. Пожалуйста, введите корректную цену."
            )

        return price
