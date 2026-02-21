import math
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q
from django.views.generic import CreateView, ListView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from books.models import Book, Category, Genre
from books.forms import BookForm

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    login_url = "/login/"

    def get_queryset(self):
        queryset = Book.objects.all()

        category_ids = self.request.GET.getlist("category_id")
        genre_ids = self.request.GET.getlist("genre_id")
        pages_choice = self.request.GET.get("pages_choice")

        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)

        if genre_ids:
            queryset = queryset.filter(genre__id__in=genre_ids).distinct()

        if pages_choice:
            if pages_choice == "1":
                queryset = queryset.filter(pages__gt=300)
            elif pages_choice == "2":
                queryset = queryset.filter(pages__lt=300)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()

        context["selected_categories"] = list(
            map(int, self.request.GET.getlist("category_id"))
        )
        context["selected_genres"] = list(
            map(int, self.request.GET.getlist("genre_id"))
        )
        context["pages_choice"] = self.request.GET.get("pages_choice")

        return context
     


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_create.html"
    success_url = reverse_lazy("books_list")

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("books_list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.profile != request.user.profile:
            return HttpResponseForbidden("Permission denied")
        return super().dispatch(request, *args, **kwargs)


class BaseView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
    pk_url_kwarg = "book_id"