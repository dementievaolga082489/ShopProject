from django.db import models


class BlogPost(models.Model):
    """Модель блоговой записи"""

    # Основные поля
    title = models.CharField("Заголовок", max_length=255, db_index=True)

    content = models.TextField("Содержимое", help_text="Основной текст блоговой записи")

    preview = models.ImageField(
        "Превью (изображение)",
        upload_to="blog/previews/%Y/%m/%d/",
        blank=True,
        null=True,
        help_text="Изображение для превью записи",
    )

    created_at = models.DateTimeField("Дата создания", auto_now_add=True, db_index=True)

    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    is_published = models.BooleanField(
        "Признак публикации",
        default=True,
        db_index=True,
        help_text="Отметьте, чтобы опубликовать запись",
    )

    views_count = models.PositiveIntegerField(
        "Количество просмотров", default=0, db_index=True
    )

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def increment_views(self):
        """Увеличивает счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=["views_count"])
