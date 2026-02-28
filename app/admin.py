from django.contrib import admin

# Register your models here.

from .models import rege,emform,category,products,cart,cart_item,address,order,orderitem

admin.site.register(rege)
admin.site.register(emform)
admin.site.register(category)
admin.site.register(products)
admin.site.register(cart)
admin.site.register(cart_item)
admin.site.register(address)
admin.site.register(order)
admin.site.register(orderitem)

