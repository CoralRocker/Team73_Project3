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
    cost = models.DecimalField(max_digits=11, decimal_places=2) # Store money up to 999,999,99.99
    type = models.TextField()
    amount = models.FloatField()
    name = models.TextField()
    ingredient = models.ForeignKey('Inventory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'customizations'

# Do we need/want a finance table???
class Finance(models.Model):
    date = models.DateField(primary_key=True)
    orders = models.TextField()  # This field type is a guess.
    revenue = models.DecimalField(max_digits=11, decimal_places=2)
    expenses = models.DecimalField(max_digits=11, decimal_places=2)
    profit = models.DecimalField(max_digits=11, decimal_places=2)
    inventory_usage = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'finances'



class Inventory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2) # Up to 999,999,999.99
    stock = models.FloatField()
    ordered = models.FloatField(blank=True, null=False)
    amount_per_unit = models.FloatField(blank=False, null=False)

    @classmethod
    def create(cls, id, name, price, stock, amount_per_unit):
        item = cls(id=id, name=name, price=price, stock=stock, ordered=0, amount_per_unit=amount_per_unit)
        item.save()
        return item

    class Meta:
        db_table = 'inventory'
    
    def __str__(self):
        return f"Inventory item {self.name} x {self.stock}"


class Menu(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)

    
    ingredients = models.ManyToManyField(Inventory, through='Ingredient')
    #models.TextField()  # This field type is a guess.
    
    size = models.TextField(blank=False, null=False)
    type = models.TextField()

    @classmethod
    def create(cls, name, price, size, type):
        item = cls(name=str(name), price=float(price), size=str(size), type=str(type))
        item.save()
        return item
    
    def addIngredient(self, ingredient: Inventory, amount : float):
        if amount <= 0:
            raise Exception(f"Invalid Argument in Menu.addIngredient: given amount is <=0!")

        self.save()

        if self.ingredient_set.filter(inventory=ingredient).count() == 0:
            _ing = Ingredient(menu_item=self, inventory=ingredient, amount=amount)
            _ing.save()
        else:
            _ing = self.ingredient_set.get(inventory=ingredient)
            _ing.amount = amount
            _ing.save()

    def getIngredientAmount(self, ingredient: Inventory) -> float:
        return self.ingredient_set.get(inventory=ingredient).amount

    def getInventoryPrice(self) -> float:
        price_aggregator = models.Sum(
                    models.ExpressionWrapper(models.F('inventory__price'),
                                             output_field=models.FloatField()) *
                    (models.F('amount') / models.F('inventory__amount_per_unit'))
                )
        return self.ingredient_set.aggregate(val=price_aggregator)['val']

    def getInventoryUsage(self) -> dict[Inventory, float]:
        usage = dict()
        for ingredient in self.ingredient_set.all():
            usage[ingredient.inventory] = ingredient.amount
        return usage

    class Meta:
        db_table = 'menu'

    def __str__(self):
        return f"Menu Item {self.id} : {self.size} {self.name}"


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)

    # Models Involved in this ingredient
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)

    # Extra Information
    amount = models.FloatField()

    def getPrice(self) -> float:
        return float(self.inventory.price) * (self.amount / self.inventory.amount_per_unit)

    def __str__(self):
        return f"Ingredient for {self.menu_item.name} :> {self.inventory.name} x {self.amount}"


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Order', models.CASCADE, null=False, related_name='items')
    menu_item = models.ForeignKey(Menu, models.CASCADE, null=False) # models.BigIntegerField(blank=True, null=True)
    customizations = models.ManyToManyField(Customization) # models.TextField(blank=True, null=True)  # This field type is a guess.
    amount = models.IntegerField(blank=False, null=False)

    class Meta:
        db_table = 'order_items'

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    cashier = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    # items = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'orders'