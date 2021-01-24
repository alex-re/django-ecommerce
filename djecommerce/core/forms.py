from django import forms
from .fields import EmptyChoiceField
from .models import Coupon, OrderProduct, STATE_CHIOSES, CITY_CHIOSES, NEIGHBOUR_CHIOSES

PAYMENT_CHOICES = (
    ('O', 'Online'),
    ('C', 'Credit Card')
)


class CheckoutForm(forms.Form):
    payment_option = EmptyChoiceField(choices=PAYMENT_CHOICES)
    state = EmptyChoiceField(choices=STATE_CHIOSES,
                             required=False, empty_label='---select---')
    city = EmptyChoiceField(choices=CITY_CHIOSES,
                            required=False, empty_label='---select---')
    neighbour = EmptyChoiceField(
        choices=NEIGHBOUR_CHIOSES, required=False, empty_label='---select---')
    postal_address = forms.CharField(
        max_length=200, required=False)
    plaque = forms.CharField(max_length=5, required=False)
    unit = forms.CharField(max_length=30, required=False)
    postal_code = forms.CharField(
        max_length=10, help_text='postal code must be 10 numbers without dash', required=False)
    receiver_fname = forms.CharField(max_length=100)
    receiver_lname = forms.CharField(max_length=100)
    receiver_national_code = forms.CharField(
        max_length=10, help_text='national code must be 10 numbers without dash')
    receiver_phone_number = forms.CharField(
        max_length=11, help_text='Example: 09123456789')
    address_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def is_valid(self):
        is_valid = super(CheckoutForm, self).is_valid()
        if not is_valid:
            return False
        address_id = self.cleaned_data.get('address_id')
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')
        neighbour = self.cleaned_data.get('neighbour')
        postal_address = self.cleaned_data.get('postal_address')
        plaque = self.cleaned_data.get('plaque')
        unit = self.cleaned_data.get('unit')
        postal_code = self.cleaned_data.get('postal_code')

        new_add_req = False
        if state or city or neighbour or postal_address or plaque or unit or postal_code:
            new_add_req = True
        if new_add_req and address_id:
            is_valid = False
        return is_valid


class CouponForm(forms.Form):
    code = forms.CharField(max_length=100)

    def is_valid(self):
        is_valid = super(CouponForm, self).is_valid()
        if not is_valid:
            return (False, '')
        code = self.cleaned_data['code']
        coupon_qs = Coupon.objects.filter(code=code)
        if coupon_qs.exists():
            return (True, coupon_qs[0])
        else:
            self.errors['invalid_coupon'] = 'Coupon does not exist; please enter valid code.'
            return (False, '')


class RefundForm(forms.Form):
    order_product_id = forms.IntegerField()
    quantity = forms.IntegerField()
    reason = forms.CharField(widget=forms.Textarea)

    def is_valid(self):
        is_valid = super(RefundForm, self).is_valid()
        if not is_valid:
            return (False, '')

        order_product_id = self.cleaned_data['order_product_id']
        quantity = self.cleaned_data['quantity']
        order_product_qs = OrderProduct.objects.filter(id=order_product_id)

        if order_product_qs.exists():
            order_product = order_product_qs[0]
            if quantity <= order_product.quantity:
                return (True, order_product)
            else:
                self.errors['invalid_order_product_quantity'] = 'your request for refund is more than order product quantity.'
                return (False, '')

        else:
            self.errors['invalid_order_product'] = 'Order Product does not exist; please enter valid id.'
            return (False, '')
