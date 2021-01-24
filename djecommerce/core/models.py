from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
STATE_CHIOSES = (
    ('TEH', 'Tehran'),
    ('KAR', 'Karaj'),
    ('ARA', 'Arak')
)
CITY_CHIOSES = (
    ('TEH', 'Tehran'),
    ('MAL', 'Malard'),
    ('AND', 'Andisheh')

)
NEIGHBOUR_CHIOSES = (
    ('APA', 'Apadana'),
    ('ARA', 'Ararat'),
    ('AZA', 'Azadi')
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    specs = models.JSONField(null=True)

    def __str__(self):
        return f'Product {self.title}'


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()

    # def get_final_price(self):
    #     if self.product.discount_price:
    #         return self.quantity * self.product.discount_price
    #     return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Order Of {self.user.username}'

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bank_account_number = models.CharField(
#         max_length=16, blank=True, null=True, help_text='for return money')


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # receiver = models.ForeignKey(
    #     'Receiver', on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=3, choices=STATE_CHIOSES)
    city = models.CharField(max_length=5, choices=CITY_CHIOSES)
    neighbour = models.CharField(max_length=5, choices=NEIGHBOUR_CHIOSES)
    postal_address = models.CharField(max_length=200)
    plaque = models.CharField(max_length=5)
    unit = models.CharField(max_length=30)
    postal_code = models.CharField(
        max_length=10, help_text='postal code must be 10 numbers without dash')
    rec_fname = models.CharField(max_length=100)
    rec_lname = models.CharField(max_length=100)
    rec_national_code = models.CharField(
        max_length=10, help_text='national code must be 10 numbers without dash')
    rec_phone_number = models.CharField(
        max_length=11, help_text='Example: 09123456789')

    def __str__(self):
        return f'Address of {self.user.username}'

# class Receiver(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     national_code = models.CharField(
#         max_length=10, help_text='national code must be 10 numbers without dash')
#     phone_number = models.CharField(
#         max_length=11, help_text='Example: 09123456789')

    # گیرنده سفارش خودم هستم
    # نام گیرنده*
    # نام خانوادگی گیرنده*
    # کد ملی گیرنده*
    # کد ملی باید ۱۰ رقم و بدون خط تیره باشد
    # شماره موبایل*
    # مثل: ۰۹۱۲۳۴۵۶۷۸۹


class Coupon(models.Model):
    '''
    Field that shows when this coupon should work
    for example if order total price greater than 100$
    Amount can be percents
    '''
    code = models.CharField(max_length=30, unique=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'Coupon: {self.code}'


class Refund(models.Model):
    '''
    Refund.objects.filter(id=1).values('order__user__username')
    '''
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    reason = models.CharField(max_length=1000)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Refund: {self.id}"
