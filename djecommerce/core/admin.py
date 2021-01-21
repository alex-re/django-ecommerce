from django.contrib import admin
from .models import Product, OrderProduct, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    # list_display_links = ('title', 'slug')


admin.site.register(Product, ProductAdmin)
admin.site.register(OrderProduct)
admin.site.register(Order)
