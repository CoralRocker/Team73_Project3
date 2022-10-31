# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Customizations(models.Model):
    id = models.BigAutoField(primary_key=True)
    cost = models.TextField()  # This field type is a guess.
    type = models.TextField()
    amount = models.DecimalField(max_digits=65535, decimal_places=65535)
    name = models.TextField()
    ingredient = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'customizations'



class Finances(models.Model):
    date = models.DateField(primary_key=True)
    orders = models.TextField()  # This field type is a guess.
    revenue = models.DecimalField(max_digits=65535, decimal_places=65535)
    expenses = models.DecimalField(max_digits=65535, decimal_places=65535)
    profit = models.DecimalField(max_digits=65535, decimal_places=65535)
    inventory_usage = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'finances'


class Inventory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=65535, decimal_places=65535)
    stock = models.FloatField()
    ordered = models.FloatField(blank=True, null=True)
    amount_per_unit = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class Menu(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=65535, decimal_places=65535)
    ingredients = models.TextField()  # This field type is a guess.
    size = models.TextField(blank=True, null=True)
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'menu'


class OrderItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    menu_id = models.BigIntegerField(blank=True, null=True)
    customizations = models.TextField(blank=True, null=True)  # This field type is a guess.
    amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    id = models.BigAutoField(primary_key=True)
    cashier = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    items = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'orders'
