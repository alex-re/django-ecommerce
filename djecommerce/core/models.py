from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
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

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return f'Order Of {self.user.username}'
