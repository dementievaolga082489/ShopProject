from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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


def contacts(request):
    # Получаем контактные данные из базы
    contacts = Contact.objects.first()

    # Получаем все категории для навигации
    categories = Category.objects.all()

    context = {
        "contacts": contacts,
        "categories": categories,
        "title": "Контакты",
    }
    return render(request, "contacts.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"Спасибо, {name}, контактный телефон - {phone}! Ваше сообщение получено."
        )
    return render(request, "contacts.html")


def products_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "products_list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "product_detail.html", context)
