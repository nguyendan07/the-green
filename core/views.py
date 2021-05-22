from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import Item, Order, OrderItem
from .templatetags import cart_template_tags


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
def quantity_plus_from_cart(request):  # quantity_plus
    slug = request.POST['slug']
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
    if order_item.item.discount or order_item.item.discount_price:
        total_item_price = order_item.get_total_discount_item_price()
    else:
        total_item_price = order_item.get_total_item_price()
    sub_total = order.get_sub_total()
    total = order.get_total()
    total_amount_saved = order.get_total_amount_saved()
    cart_item_count = cart_template_tags.cart_item_count(request.user)
    return JsonResponse(
        {
            'quantity': order_item.quantity,
            'total_item_price': total_item_price,
            'total_amount_saved': total_amount_saved,
            'sub_total': sub_total,
            'total': total,
            'cart_item_count': cart_item_count
        })
    # return redirect("core:product-detail", slug=slug)


@login_required
def quantity_minus_from_cart(request):
    slug = request.POST['slug']
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                          user=request.user,
                                                          ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                if order_item.item.discount or order_item.item.discount_price:
                    total_item_price = order_item.get_total_discount_item_price()
                else:
                    total_item_price = order_item.get_total_item_price()
                sub_total = order.get_sub_total()
                total = order.get_total()
                total_amount_saved = order.get_total_amount_saved()
                return JsonResponse(
                    {
                        'quantity': order_item.quantity,
                        'total_item_price': total_item_price,
                        'total_amount_saved': total_amount_saved,
                        'sub_total': sub_total,
                        'total': total
                    })
            else:
                order.items.remove(order_item)
                sub_total = order.get_sub_total()
                total = order.get_total()
                total_amount_saved = order.get_total_amount_saved()

                return JsonResponse(
                    {
                        'remove': True,
                        'total_amount_saved': total_amount_saved,
                        'sub_total': sub_total,
                        'total': total
                    })


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)

    return redirect('core:checkout-cart')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')
