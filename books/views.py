
import math
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from books.forms import CreatBooksForms
from django.views.generic import CreateView, ListView, DeleteView,DetailView,TemplateView
from books.models import Book, Category,Genre
from books.forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
# Create your views here.
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    login_url = "/login/"

    def get_queryset(self):
        queryset = Book.objects.all()

        search_query = self.request.GET.get("search", "")
        category_ids = self.request.GET.getlist("category_id")
        genre_ids = self.request.GET.getlist("genre_id")
        episodes_choice = self.request.GET.get("episodes_choice")

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)

        if genre_ids:
            queryset = queryset.filter(genre__id__in=genre_ids).distinct()

        if episodes_choice:
            if episodes_choice == "1":
                queryset = queryset.filter(episodes__gt=100)
            elif episodes_choice == "2":
                queryset = queryset.filter(episodes__lt=100)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["forms"] = SearchForm(self.request.GET or None)
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()

        context["selected_categories"] = list(
            map(int, self.request.GET.getlist("category_id"))
        )
        context["selected_genres"] = list(
            map(int, self.request.GET.getlist("genre_id"))
        )
        context["search_query"] = self.request.GET.get("search", "")
        context["episodes_choice"] = self.request.GET.get("episodes_choice")

        return context

