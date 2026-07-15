from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogPostCreateView, BlogPostDetailView, BlogPostListView, BlogPostDeleteView, BlogPostUpdateView

app_name = BlogConfig.name

urlpatterns = [
    # Список всех записей
    path('', BlogPostListView.as_view(), name='post_list'),

    # Детальная страница записи
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),

    # Создание записи
    path('post/create/', BlogPostCreateView.as_view(), name='post_create'),

    # Редактирование записи
    path('post/<int:pk>/update/', BlogPostUpdateView.as_view(), name='post_update'),

    # Удаление записи
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_confirm_delete'),]