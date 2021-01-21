from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
# from django.views.generic import View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Product, OrderProduct, Order
from .serializers import ProductSerializer, OrderSerializer


def home(request):
    '''
    returns jsonify of all products
    '''
    serializer = ProductSerializer(Product.objects.all(), many=True)
    data = {
        'products': serializer.data
    }
    return JsonResponse(data)


@login_required
def order_summary(request):
    try:
        order_serializer = OrderSerializer(
            Order.objects.get(user=request.user, ordered=False))
        data = {
            'order': order_serializer.data,
        }
        return JsonResponse(data)

    except Order.DoesNotExist:
        data = {
            'error': 'You do not have an active order'
        }
        return JsonResponse(data)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_serializer = ProductSerializer(product)
    data = {
        'product': product_serializer.data
    }
    return JsonResponse(data)


@login_required
def add_to_cart(request, slug):
    '''
    If user has more than one active order
        recognizes the problem
    else if user did not have an active order
        create one and add product to his order
    else if user has an active order
        if the order product was in the order
            increase the quantity
        else
            add product to order
    '''
    product = get_object_or_404(Product, slug=slug)
    pro_ser_data = ProductSerializer(product).data
    order_product, created = OrderProduct.objects.get_or_create(
        user=request.user,
        product=product,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    n_orders = order_qs.count()

    # if (n_orders := order_qs.count()) > 1:
    if n_orders > 1:
        data = {'error': f'You have {n_orders} active orders!'}
        return JsonResponse(data)

    # elif order_qs.exists():
    elif n_orders == 1:
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            data = {
                'message': f'the fallowing product quantity was updated to {order_product.quantity}',
                'product': pro_ser_data
            }
            return JsonResponse(data)
        else:
            order.products.add(order_product)
            data = {
                'message': 'This item was added to your cart.',
                'product': pro_ser_data
            }
            return JsonResponse(data)
    # else:
    elif n_orders == 0:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        data = {
            'message': 'Order created for you and the fallowing product was added to your cart.',
            'product': pro_ser_data
        }
        return JsonResponse(data)
