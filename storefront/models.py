from django.db import models
import datetime


class Customization(models.Model):
    id = models.BigAutoField(primary_key=True)
    cost = models.DecimalField(max_digits=11, decimal_places=2) # Store money up to 999,999,99.99
    type = models.TextField()
    amount = models.FloatField()
    name = models.TextField(default='')
    ingredient = models.ForeignKey('Inventory', on_delete=models.CASCADE)

    def getInventoryPrice(self) -> float:
        return self.amount / self.ingredient.amount_per_unit * float(self.ingredient.price)

    class Meta:
        db_table = 'customizations'
        
    def __str__(self):
        return f"{self.name}"

# Do we need/want a finance table???
class Finance(models.Model):
    date = models.DateField(primary_key=True)

    revenue = models.DecimalField(max_digits=11, decimal_places=2)
    expenses = models.DecimalField(max_digits=11, decimal_places=2)
    profit = models.DecimalField(max_digits=11, decimal_places=2)
    
    @classmethod
    def create(cls, date=datetime.date.today()):
        try:
            item = Finance(date=date, revenue=0,expenses=0,profit=0)
            item.save()
            return item
        except:
            return Finance.objects.get(pk=date)

    def getOrders(self):
        return Order.objects.filter(date=self.pk)

    def getExpenses(self):
        invPrice = models.Sum(models.ExpressionWrapper(
            models.F('orderitem__menu_item__ingredients__price'),
            output_field=models.FloatField()) * 
                              (models.F('orderitem__menu_item__ingredient__amount') /
                              models.F('orderitem__menu_item__ingredients__amount_per_unit'))
            )
        
        self.expenses = self.getOrders().aggregate(price=invPrice)['price']

        return self.expenses

    def getRevenue(self):
        rev = models.Sum(models.ExpressionWrapper(models.F('orderitem__cost'),
                                                  output_field=models.FloatField()))
        self.revenue = self.getOrders().aggregate(price=rev)['price']

        return self.revenue

    def getProfit(self):
        self.getExpenses()
        self.getRevenue()
        
        self.profit = self.revenue - self.expenses

        return self.profit

    def getInventoryUsage(self):

        return None

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
    def removeFromInv(cls, inv):
        objs = list()
        for key in inv:
            objs.append(key)
            key.stock -= inv[key]

        cls.objects.bulk_update(objs, ['stock'])


    @classmethod
    def create(cls, id, name, price, stock, amount_per_unit):
        item = cls(id=id, name=name, price=price, stock=stock, ordered=0, amount_per_unit=amount_per_unit)
        item.save()
        return item

    class Meta:
        db_table = 'inventory'
    
    def __str__(self):
        return f"{self.name} x {self.stock}"


class Menu(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.TextField(default="Lorem")

    
    ingredients = models.ManyToManyField(Inventory, through='Ingredient')
    #models.TextField()  # This field type is a guess.
    
    size = models.TextField(blank=False, null=False)
    type = models.TextField()
    
    image = models.TextField(null=True)


    @classmethod
    def create(cls, name, price, size, type, image):
        item = cls(name=str(name), price=float(price), size=str(size), type=str(type), image=image)
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
        return f"{self.id} : {self.size} {self.name}"


class Ingredient(models.Model):
    id = models.BigAutoField(primary_key=True)

    # Models Involved in this ingredient
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)

    # Extra Information
    amount = models.FloatField()

    def getPrice(self) -> float:
        return round(float(self.inventory.price) * (self.amount / self.inventory.amount_per_unit),2)

    def __str__(self):
        return f"{self.menu_item.name} :> {self.inventory.name} x {self.amount}"


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)

    # Order this item belongs to
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=False)

    # Menu Item that this item represents
    menu_item = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, null=False) 

    # Customizations Added to the item
    customizations = models.ManyToManyField(Customization, through='ItemCustomization') 

    # Amount of item requested
    amount = models.IntegerField(blank=False, null=False)

    # Price paid by the customer
    cost = models.DecimalField(max_digits=11, decimal_places=2)

    @classmethod
    def create(cls, order, menu_item, amount=1):
        item = cls(order=order, menu_item=menu_item, amount=amount)
        item.cost = menu_item.price * amount
        item.save()
        return item

    def getInventoryPrice(self) -> float:
        custPrice = 0.0
        for cust in self.customizations.all():
            custPrice += cust.getInventoryPrice() 

        return self.amount * (self.menu_item.getInventoryPrice() + custPrice)

    def getInventoryUsage(self) -> dict[Inventory, float]:
        # Get Item Usage
        menu_usage = self.menu_item.getInventoryUsage()

        # Add customization usages
        for cust in self.itemcustomization_set.all():
            cust_obj = cust.customization

            if cust_obj.ingredient in menu_usage:
                menu_usage[cust_obj.ingredient] += cust.amount * cust_obj.amount
            else:
                menu_usage[cust_obj.ingredient] = cust_obj.amount * cust.amount

        
        # Add amount multiplier
        for key in menu_usage:
            menu_usage[key] *= self.amount

        return menu_usage


    def getPriceList(self):
        plist = dict()

        foundFoam = False
        foundSauce = False
        foundSyrup = False

        custCost = 0.0

        for cust_obj in self.itemcustomization_set.all():
            cust = cust_obj.customization

            if cust.type.lower() == "syrup":
                if foundSyrup:
                    plist[cust_obj] = 0.0
                else:
                    foundSyrup = True
                    plist[cust_obj] = float(cust.cost)

            elif cust.type.lower() == 'sauce':
                if foundSauce:
                    plist[cust_obj] = 0.0
                else:
                    foundSauce = True
                    plist[cust_obj] = float(cust.cost)
            elif cust.type.lower() == 'foam':
                if foundFoam:
                    plist[cust_obj] = 0.0
                else:
                    foundFoam = True
                    plist[cust_obj] = float(cust.cost)
            else:
                plist[cust_obj] = float(cust.cost)


        return plist


    def getCustomizationPrice(self) -> float:

        foundFoam = False
        foundSauce = False
        foundSyrup = False

        custCost = 0.0

        for cust in self.itemcustomization_set.all():
            cust = cust.customization

            if not foundSyrup and cust.type.lower() == "syrup":
                foundSyrup = True
                custCost += float(cust.cost)
            elif not foundSauce and cust.type.lower() == 'sauce':
                foundSauce = True
                custCost += float(cust.cost)
            elif not foundFoam and cust.type.lower() == 'foam':
                foundFoam = True
                custCost += float(cust.cost)
            else:
                custCost += float(cust.cost)

        return custCost

    def getPrice(self) -> float:
        return float(self.cost)

    def addCustomization(self, cust :Customization, amount :float):
        newCust = ItemCustomization(order_item=self, customization=cust, amount=amount)
        newCust.save()

        self.cost = self.amount * (self.getCustomizationPrice() + self.menu_item.price)
        return

    class Meta:
        db_table = 'order_items'
        
    def __str__(self):
        return f"{self.menu_item} : {self.amount}"

class ItemCustomization(models.Model):
    id = models.BigAutoField(primary_key=True)
    
    order_item = models.ForeignKey(OrderItem, models.CASCADE)
    customization = models.ForeignKey(Customization, models.CASCADE)

    amount = models.IntegerField(null=False, blank=False)
    
    def getInventoryPrice(self) -> float:
        return self.customization.getInventoryPrice() * self.amount

    def getCustomizationPrice(self) -> float:

        custCost = 0.0

        for i in range(self.amount):
            cust = self.customization

            if cust.type.lower() == "syrup":
                custCost = float(cust.cost)
                break
            elif cust.type.lower() == 'sauce':
                custCost = float(cust.cost)
                break
            elif cust.type.lower() == 'foam':
                custCost = float(cust.cost)
                break;
            else:
                custCost += float(cust.cost)

        return round(custCost,2)

    def __str__(self):
        return f"{self.order_item.menu_item.name} :> {self.customization.name} {self.customization.type} x {self.amount}"

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    cashier = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    items = models.ManyToManyField(Menu, through='OrderItem')


    # price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    # items = models.TextField(blank=True, null=True)  # This field type is a guess.

    def getInventoryUsage(self) -> dict[Inventory, float]:
        inv = dict()
        for item in self.orderitem_set.all():
            invSum(inv, item.getInventoryUsage())

        return inv
            
    def getInventoryPrice(self) -> float:
        invPrice = 0.0
        for item in self.orderitem_set.all():
            invPrice += item.getInventoryPrice()
        return invPrice


    def getPrice(self) -> float:
        price = 0.0
        for item in self.orderitem_set.all():
            price += item.getPrice()

        return round(price,2)

    @classmethod
    def create(cls, cashier :str, date = datetime.datetime.now()):
        ordr = cls(cashier=cashier, date=date)
        ordr.save()
        return ordr


    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"{self.date}"

'''
Add two Inventory dictionaries. Add inv to out. Doesn't return anything. Modifies out.
'''
def invSum(out :dict[Inventory,float], inv :dict[Inventory, float]):

    for key in inv:
        if key in out:
            out[key] += inv[key]
        else:
            out[key] = inv[key]
