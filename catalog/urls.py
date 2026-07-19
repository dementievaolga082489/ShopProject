from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    home,
    ProductListView,
    ProductDetailView,
    ContactView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = CatalogConfig.name
urlpatterns = [
    path("home/", home, name="home"),
    #  path("contacts/", contacts, name="contacts"),
    path("contact/", ContactView.as_view(), name="contacts"),
    path("", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "post/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_confirm_delete",
    ),
]
