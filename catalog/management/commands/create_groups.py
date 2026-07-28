from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу Модератор продуктов'

    def handle(self, *args, **options):
        # Получаем права
        content_type = ContentType.objects.get_for_model(Product)

        can_unpublish = Permission.objects.get(
            content_type=content_type,
            codename='can_unpublish_product'
        )
        delete_product = Permission.objects.get(
            content_type=content_type,
            codename='delete_product'
        )

        # Создаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        group.permissions.add(can_unpublish, delete_product)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана!'))