from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('order-summary/', order_summary, name='order-summary'),
    path('product/<slug>/', product_detail, name='product-detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-product-from-cart/<slug>/',
         remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')

]

# urlpatterns = [
#     path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
# ]