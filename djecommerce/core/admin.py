from django.contrib import admin
from .models import Product, OrderProduct, Order, Address, Coupon, Refund  # , Receiver


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    # list_display_links = ('title', 'slug')


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')


admin.site.register(Product, ProductAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order)
admin.site.register(Address)
# admin.site.register(Receiver)
admin.site.register(Coupon)
admin.site.register(Refund)
