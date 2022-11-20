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
    search_fields = ['id', 'name__icontains', 'size__iexact', 'price', 'type__iexact']

class CustomizationAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name__icontains', 'type__iexact']

# Register your models here.
admin.site.register(Customization, CustomizationAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Finance)
admin.site.register(Inventory)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Ingredient)

