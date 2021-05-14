from django.urls import path

from . import views

app_name = 'core'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop', views.ItemListView.as_view(), name='shop'),
    path('contact', views.contact, name='contact'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product-detail'),
    path('checkout/cart', views.OrderSummaryView.as_view(), name='checkout-cart'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
]
