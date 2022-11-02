from django.contrib import admin

from .models import Customizations, Orders, OrderItems, Finances, Inventory, Menu

# Register your models here.
admin.site.register(Customizations)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(Finances)
admin.site.register(Inventory)
admin.site.register(Menu)
