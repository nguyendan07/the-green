from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Item, OrderItem


class HomeView(ListView):
    model = Item
    template_name = 'index.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-single.html'
