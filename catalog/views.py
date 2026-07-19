from gettext import Catalog
from idlelib.textview import ViewWindow

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    View,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.forms import ProductForm
from catalog.models import Product, Category, Contact


def home(request):
    # Получаем последние 5 созданных продуктов
    latest_products = Product.objects.all().order_by("-created_at")[:5]

    # Вывод в консоль (для отладки)
    for i, product in enumerate(latest_products, 1):
        print(f"{i}. {product.name}")
        print(f"Цена: {product.price} руб.")
        print(f"Категория: {product.category.name}")
        print(f"Создан: {product.created_at.strftime('%d.%m.%Y %H:%M')}")

    return render(request, "home.html", {"latest_products": latest_products})


class ContactView(View):
    """Страница контактов с использованием View"""

    def get(self, request, *args, **kwargs):
        # Получаем контактные данные из базы
        contacts = Contact.objects.first()

        # Получаем все категории для навигации
        categories = Category.objects.all()

        context = {
            "contacts": contacts,
            "categories": categories,
            "title": "Контакты",
        }

        return render(request, "catalog/contacts.html", context)

    # def contacts(request):
    # Получаем контактные данные из базы
    #    contacts = Contact.objects.first()

    # Получаем все категории для навигации
    #    categories = Category.objects.all()

    #    context = {
    #        "contacts": contacts,
    #        "categories": categories,
    #        "title": "Контакты",
    #    }
    #    return render(request, "contacts.html", context)

    def post(self, request, *args, **kwargs):
        # Обработка отправки формы обратной связи
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Здесь можно отправить письмо или сохранить в БД
        messages.success(request, "Ваше сообщение отправлено!")

        return self.get(request, *args, **kwargs)


# def contact(request):
#    if request.method == "POST":
#        name = request.POST.get("name")
#        phone = request.POST.get("phone")
#        message = request.POST.get("message")
#        return HttpResponse(
#            f"Спасибо, {name}, контактный телефон - {phone}! Ваше сообщение получено."
#        )
#    return render(request, "contacts.html")


class ProductListView(ListView):
    model = Product


# def products_list(request):
#    products = Product.objects.all()
#    context = {"products": products}
#    return render(request, "product_list.html", context)


class ProductDetailView(DetailView):
    model = Product


# def product_detail(request, pk):
#    product = get_object_or_404(Product, pk=pk)
#    context = {"product": product}
#    return render(request, "product_detail.html", context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "catalog/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")
