from django.urls import path 

from .views import AddToCart
from  django.conf import settings
from django.conf.urls.static import static

from .views import view_cart, get_cart_item_count

urlpatterns = [
    path('', view_cart, name = 'view_cart'),
    path('add/', AddToCart.as_view(), name = 'add_to_cart'),
    path('cart/count/',get_cart_item_count, name = 'cart_count')
]