from django.urls import path

from . import views

app_name = 'core'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop', views.ItemListView.as_view(), name='shop'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product-detail'),
    path('checkout/cart', views.OrderSummaryView.as_view(), name='checkout-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
    path('quantity-minus-from-cart',
         views.quantity_minus_from_cart, name='quantity-minus-from-cart'),
    path('quantity-plus-from-cart',
         views.quantity_plus_from_cart, name='quantity-plus-from-cart'),
]
