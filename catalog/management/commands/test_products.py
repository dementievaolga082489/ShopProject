from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Загружает тестовые данные из фикстуры"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "categories.json")
        self.stdout.write(self.style.SUCCESS("Успешно загружено из фикстуры"))

        call_command("loaddata", "products.json")
        self.stdout.write(self.style.SUCCESS("Успешно загружено из фикстуры"))
