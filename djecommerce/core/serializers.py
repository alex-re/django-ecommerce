from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, OrderProduct, Order

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.Serializer):
    products = ProductSerializer(required=False, many=True)
    user = UserSerializer(required=False)

    class Meta:
        model = Order
        fields = '__all__'
