# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Customization(models.Model):
    id = models.BigAutoField(primary_key=True)
    cost = models.TextField()  # This field type is a guess.
    type = models.TextField()
    amount = models.DecimalField(max_digits=65535, decimal_places=65535)
    name = models.TextField()
    ingredient = models.IntegerField()

    class Meta:
        db_table = 'customizations'

    def __str__(self):
        return self.name[:50]

 
class Finance(models.Model):
    date = models.DateField(primary_key=True)
    orders = models.TextField()  # This field type is a guess.
    revenue = models.DecimalField(max_digits=65535, decimal_places=65535)
    expenses = models.DecimalField(max_digits=65535, decimal_places=65535)
    profit = models.DecimalField(max_digits=65535, decimal_places=65535)
    inventory_usage = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'finances'
    
    def __str__(self):
        return self.orders[:50]


class InventoryItem(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=65535, decimal_places=65535)
    stock = models.FloatField()
    ordered = models.FloatField(blank=True, null=True)
    amount_per_unit = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'inventory'
    
    def __str__(self):
        return self.name[:50]


class MenuItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=65535, decimal_places=65535)
    ingredients = models.TextField()  # This field type is a guess.
    size = models.TextField(blank=True, null=True)
    type = models.TextField()

    class Meta:
        db_table = 'menu'
    
    def __str__(self):
        return self.name[:50]


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.CASCADE, null=False, related_name='items')
    menu_item = models.ForeignKey(Menu, models.CASCADE, null=False) # models.BigIntegerField(blank=True, null=True)
    customizations = models.ManyToManyField(Customizations) # models.TextField(blank=True, null=True)  # This field type is a guess.
    amount = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return self.menu_id[:50]


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    cashier = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    # items = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'orders'
    
    def __str__(self):
        return self.date[:50]
