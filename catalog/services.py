from django.core.cache import cache

from catalog.models import Category, Product
from config.settings import CACHE_ENABLED


class ProductService:
    """Сервис для работы с продуктами"""

    @staticmethod
    def _get_products_query(category):
        """
        Внутренний метод для построения QuerySet продуктов категории
        """
        return (
            Product.objects.filter(
                category=category,
            )
            .select_related("category")
            .order_by("-created_at")
        )

    @staticmethod
    def get_products_by_category(category_id):
        """
        Получить все продукты в категории по ID
        """
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Product.objects.none()
        products = list(ProductService._get_products_query(category))

        if not CACHE_ENABLED:

            return products

        # Ключ для кеширования
        cache_key = f"products_category_{category_id}"

        # Пытаемся получить из кеша
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        # Кешируем на 15 минут
        cache.set(cache_key, products, 60 * 15)

        return products

    @staticmethod
    def get_all_products_cached():
        """
        НИЗКОУРОВНЕВОЕ КЕШИРОВАНИЕ: Получить все продукты.
        """
        cache_key = "all_products"

        # Пытаемся получить из кеша
        if CACHE_ENABLED:
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data

        # Получаем из базы
        products = list(Product.objects.all())

        # Сохраняем в кеш
        if CACHE_ENABLED:
            cache.set(cache_key, products, 60 * 15)

        return products
