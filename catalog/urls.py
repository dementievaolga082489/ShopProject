from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (ContactView, ProductCreateView, ProductDeleteView,
                           ProductDetailView, ProductListView,
                           ProductUpdateView, category_products_view, home,
                           toggle_publish)

app_name = CatalogConfig.name
urlpatterns = [
    path("home/", home, name="home"),
    #  path("contacts/", contacts, name="contacts"),
    path("contact/", ContactView.as_view(), name="contacts"),
    path("", ProductListView.as_view(), name="products_list"),
    path(
        "products/<int:pk>/",
        cache_page(60)(ProductDetailView.as_view()),
        name="product_detail",
    ),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("product/<int:pk>/toggle-publish/", toggle_publish, name="toggle_publish"),
    path(
        "category/<int:category_id>/", category_products_view, name="category_products"
    ),
]
