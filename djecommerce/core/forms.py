from django import forms
from .models import STATE_CHIOSES, CITY_CHIOSES, NEIGHBOUR_CHIOSES

PAYMENT_CHOICES = (
    ('O', 'Online'),
    ('C', 'Credit Card')
)


class CheckoutForm(forms.Form):
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES)
    state = forms.ChoiceField(choices=STATE_CHIOSES, required=False)
    city = forms.ChoiceField(choices=CITY_CHIOSES, required=False)
    neighbour = forms.ChoiceField(choices=NEIGHBOUR_CHIOSES, required=False)
    postal_address = forms.CharField(max_length=200, required=False)
    plaque = forms.CharField(max_length=5, required=False)
    unit = forms.CharField(max_length=30, required=False)
    postal_code = forms.CharField(max_length=10, help_text='postal code must be 10 numbers without dash', required=False)
    receiver_fname = forms.CharField(max_length=100)
    receiver_lname = forms.CharField(max_length=100)
    receiver_national_code = forms.CharField(max_length=10, help_text='national code must be 10 numbers without dash')
    receiver_phone_number = forms.CharField(max_length=11, help_text='Example: 09123456789')
    address_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    # TODO:
    # def is_valid(self):
        # pass


