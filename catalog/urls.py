from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import  home, ProductListView, ProductDetailView, ContactView

app_name = CatalogConfig.name
urlpatterns = [
    path("home/", home, name="home"),
  #  path("contacts/", contacts, name="contacts"),
    path("contact/", ContactView.as_view(), name="contacts"),
    path("", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
