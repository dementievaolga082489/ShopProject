from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import BlogPost


class BlogPostListView(ListView):
    """Список всех опубликованных записей блога"""

    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Фильтрация записей"""
        queryset = BlogPost.objects.filter(is_published=True)
        return queryset


class BlogPostDetailView(DetailView):
    """Детальная страница блоговой записи"""

    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров"""
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj


class BlogPostCreateView(CreateView):
    """Создание новой записи"""

    model = BlogPost
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post_list")
    fields = ["title", "content", "preview", "is_published"]


class BlogPostUpdateView(UpdateView):
    """Редактирование записи"""

    model = BlogPost
    template_name = "blog/post_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Удаление записи"""

    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog:post_list")
