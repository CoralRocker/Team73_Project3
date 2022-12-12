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
class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name__icontains', 'size__iexact', 'price', 'type__iexact']
    inlines = (IngredientInline,)

class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'stock', 'amount_per_unit', 'price']

class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['id', 'menu_item__name', 'inventory__name']
    fields = ['menu_item', 'inventory', 'amount']
    readonly_fields = tuple()

    def has_add_permission(self, request):
        return True

class CustomizationAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name__icontains', 'type__iexact']

# Register your models here.
admin.site.register(Customization, CustomizationAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Finance)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Ingredient, IngredientAdmin)

