from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, OrderProduct, Order, Address  # , Receiver
from .serializers import ProductSerializer, OrderSerializer
from .forms import CheckoutForm, CouponForm, RefundForm


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


@login_required
def remove_from_cart(request, slug):
    '''
    completely remove order product from order without considering quantity
    '''
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    n_orders = order_qs.count()
    if n_orders == 1:
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product, user=request.user, ordered=False)[0]
            order.products.remove(order_product)
            order_product.delete()
            data = {
                'message': 'This item was removed from your cart.'
            }
            return JsonResponse(data)
        else:
            data = {
                'error': 'This item was not in your cart'
            }
            return JsonResponse(data)
    else:
        data = {
            'error': f'Number of your active orders: {n_orders}'
        }
        return JsonResponse(data)


@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    n_orders = order_qs.count()
    if n_orders == 1:
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product, user=request.user, ordered=False)[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
                data = {
                    'message': f'Product quantity was updated to {order_product.quantity}.'
                }
                return JsonResponse(data)
            else:
                order.products.remove(order_product)
                order_product.delete()
                data = {
                    'message': 'order_product removed from your order'
                }
                return JsonResponse(data)
        else:
            data = {
                'message': 'This item was not in your cart'
            }
            return JsonResponse(data)
    else:
        data = {
            'error': f'Number of your active orders: {n_orders}'
        }
        return JsonResponse(data)


@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class CheckoutView(View):
    '''
    TODO: when the user want to recive his order
    electronic payment
        discount code
        electronic payment gateway
    pay with credit card
        discount code
    '''
    login_required = True

    def get(self, request):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order
            }
            address_qs = Address.objects.filter(user=request.user)
            if address_qs.exists():
                context.update({
                    'addresses': address_qs
                })
            return render(request, "core/checkout.html", context)
        except Order.DoesNotExist:
            messages.warning(request, "You do not have an active order")
            return redirect("core:home")

    def post(self, request):
        form = CheckoutForm(request.POST)
        # form.is_valid()
        # return JsonResponse(form.cleaned_data)
        try:
            order = Order.objects.get(user=request.user, ordered=False)

        except Order.DoesNotExist:
            return JsonResponse({'error': 'You do not have an active order'})

        if form.is_valid():
            # create receiver
            # receiver_fname = form.cleaned_data['receiver_fname']
            # receiver_lname = form.cleaned_data['receiver_lname']
            # receiver_national_code = form.cleaned_data['receiver_national_code']
            # receiver_phone_number = form.cleaned_data['receiver_phone_number']
            # receiver = Receiver.objects.create(first_name=receiver_fname, last_name=receiver_lname,
            #                                    national_code=receiver_national_code, phone_number=receiver_phone_number)
            # create address with receiver

            if 'address_id' in form.cleaned_data:
                address = Address.objects.get(
                    id=form.cleaned_data['address_id'])
            else:
                state = form.cleaned_data['state']
                city = form.cleaned_data['city']
                neighbour = form.cleaned_data['neighbour']
                postal_address = form.cleaned_data['postal_address']
                plaque = form.cleaned_data['plaque']
                unit = form.cleaned_data['unit']
                postal_code = form.cleaned_data['postal_code']
                rec_fname = form.cleaned_data['receiver_fname']
                rec_lname = form.cleaned_data['receiver_lname']
                rec_national_code = form.cleaned_data['receiver_national_code']
                rec_phone_number = form.cleaned_data['receiver_phone_number']
                address = Address.objects.create(user=request.user, state=state, city=city, neighbour=neighbour,
                                                 postal_address=postal_address, plaque=plaque, unit=unit, postal_code=postal_code,
                                                 rec_fname=rec_fname, rec_lname=rec_lname, rec_national_code=rec_national_code, rec_phone_number=rec_phone_number)
            # assign the address to the order
            order.address = address
            order.save()
            payment_option = form.cleaned_data['payment_option']
            if payment_option == "C":
                # user want to pay with credit card
                # process the product for transportation
                return JsonResponse({'message': 'Your order was saved and it will process for transfer.'})
            elif payment_option == "O":
                # TODO: shaparak
                return HttpResponse('shaparak')
            else:
                return JsonResponse({'error': 'Invalid payment option selected'})
        else:
            return JsonResponse({'errors': form.errors, 'data': form.cleaned_data})


class AddCouponView(View):
    def get(self, request):
        form = CouponForm()
        context = {'form': form}
        return render(request, 'core/add_coupon.html', context)

    def post(self, request):
        form = CouponForm(request.POST)
        is_valid, coupon = form.is_valid()
        if is_valid:
            try:
                order = Order.objects.get(user=request.user, ordered=False)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'You dont have an active order'})
            order.coupon = coupon
            order.save()
            messages.success(request, 'Coupon added for you.')
            return redirect('core:checkout')
        else:
            return JsonResponse({'errors': form.errors, 'data': form.cleaned_data})


class RequestRefundView(View):
    def get(self, request):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, request):
        form = RefundForm(request.POST)
        is_valid, order_product = form.is_valid()
        if form.is_valid:
            order_product.refund_requested = True
            order_product.save()

            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']
            refund = Refund(order_product=order_product,
                            quantity=quantity, reason=reason)
            refund.save()
        else:
            return JsonResponse({'errors': form.errors, 'data': form.cleaned_data})
