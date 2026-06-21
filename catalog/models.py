from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование продукта",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="catalog/images",
        blank=True,
        null=True,
        verbose_name="Изображение продукта",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория продукта",
        help_text="Введите категорию продукта",
        blank=True,
        null=True,
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания продукта",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category", "price", "created_at", "updated_at"]

    def __str__(self):
        if self.category:
            return f"{self.name} ({self.category})"
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Категория продукта",
        help_text="Введите категорию продукта",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
