from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Item, Order, OrderItem


class HomeView(ListView):
    model = Item
    template_name = 'index.html'

    # def get_queryset(self) -> QuerySet:
    #     return super().get_queryset()


class ItemListView(ListView):
    model = Item
    paginate_by = 12
    ordering = ['-id']
    template_name = 'shop.html'


class OrderSummaryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'cart.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        try:
            return Order.objects.get(user=self.request.user, ordered=False)
        except Order.DoesNotExist:
            return None


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-single.html'


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                          user=request.user,
                                                          ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:product-detail", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = Order.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

    return redirect('core:product-detail')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')
