from django.contrib import admin
from LittleLemonAPI.models import Order, Category, OrderItem, MenuItem,  Cart

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)