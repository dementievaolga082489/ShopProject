from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from catalog.forms import ProductForm
from catalog.models import Category, Contact, Product
from catalog.services import ProductService


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
    template_name = 'catalog/product_list.html'
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Добавляем права для каждого продукта
        for product in context["products"]:
            product.can_edit = user.is_authenticated and product.owner == user
            product.can_delete = user.is_authenticated and (
                product.owner == user or user.has_perm("catalog.can_unpublish_product")
            )
        return context

    def get_queryset(self):
        return ProductService.get_all_products_cached()


# def products_list(request):
#    products = Product.objects.all()
#    context = {"products": products}
#    return render(request, "product_list.html", context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        product = self.object

        context["can_edit"] = user.is_authenticated and product.owner == user
        context["can_delete"] = user.is_authenticated and (
            product.owner == user or user.has_perm("catalog.can_unpublish_product")
        )
        return context


def toggle_publish(request, pk):
    """Переключение статуса публикации"""
    product = get_object_or_404(Product, pk=pk)

    # Проверяем права
    if product.owner != request.user and not request.user.has_perm(
        "catalog.can_unpublish_product"
    ):
        messages.error(request, "Нет прав для изменения статуса")
        return redirect("catalog:products_list")

    product.is_published = not product.is_published
    product.save()

    messages.success(request, f"Статус публикации изменен")
    return redirect("catalog:products_list")


# def product_detail(request, pk):
#    product = get_object_or_404(Product, pk=pk)
#    context = {"product": product}
#    return render(request, "product_detail.html", context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "catalog/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        # Только владелец может редактировать
        if product.owner != request.user:
            messages.error(request, "Вы можете редактировать только свои продукты.")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        # Владелец или модератор может удалять
        if product.owner != request.user and not request.user.has_perm(
            "catalog.can_unpublish_product"
        ):
            messages.error(request, "У вас нет прав для удаления.")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def category_products_view(request, category_id):
    """
    Отображение продуктов по категории
    """
    category = get_object_or_404(Category, id=category_id)
    products = ProductService.get_products_by_category(category_id)

    context = {
        "category": category,
        "products": products,
        "all_categories": Category.objects.all(),  # Для навигации
    }

    return render(request, "catalog/products_by_category.html", context)
