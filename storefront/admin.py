from django.contrib import admin

from .models import (
    Customization, 
    Order, 
    OrderItem, 
    Finance, 
    Inventory, 
    Menu,
    Ingredient
)

# Register your models here.
admin.site.register(Customization)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Finance)
admin.site.register(Inventory)
admin.site.register(Menu)
admin.site.register(Ingredient)

