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

class MenuAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name__icontains', 'size', 'price', 'type']

# Register your models here.
admin.site.register(Customization)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Finance)
admin.site.register(Inventory)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Ingredient)

