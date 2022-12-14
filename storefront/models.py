from django.db.models import *
from django.db import connection
import itertools
import datetime

## 
# @brief Customization Model Class
# 
# The role of this model is to hold the information about each individual customization that
# is available to the customer.
# 
# The model is related to the Inventory Model, which allows customizations to draw their
# ingredients from the store's inventory.
class Customization(Model):

    ## ID of the customization
    id = BigAutoField(primary_key=True)

    ## Cost of the customization
    cost = DecimalField(max_digits=11, decimal_places=2) # Store money up to 999,999,99.99

    ## Internal type of the customization. Affects its price
    type = TextField()

    ## Amount of the required ingredient to be used. Grams
    amount = FloatField()

    ## Name of the customization that the customer sees
    name = TextField(default='')

    ## Inventory item that the customization uses
    ingredient = ForeignKey('Inventory', on_delete=CASCADE)

    ## 
    # Get the cost to restock the given amount of the customization
    # 
    # @param cust_amount The amount of customizations to get the cost for.
    def getInventoryPrice(self, cust_amount=1) -> float:

        return cust_amount * (self.amount / self.ingredient.amount_per_unit) * float(self.ingredient.price)

    class Meta:
        db_table = 'customizations'
        
    def __str__(self):
        return f"{self.name}"

## Finance Model Class
#
# The Finance Model contains useful aggregate functions which allow it to
# calculate various reports for the end user. This model stores a date, as
# well as the profit, revenue, and expenses for that date. 
class Finance(Model):

    ## Date that the finance row represents
    date = DateField(primary_key=True)

    ## Revenue in dollars for that day
    revenue = DecimalField(blank=True, max_digits=11, decimal_places=2)

    ## Expenses in dollars for that day
    expenses = DecimalField(blank=True, max_digits=11, decimal_places=2)

    ## Profit in dollars for that day
    profit = DecimalField(blank=True, max_digits=11, decimal_places=2)

    ##
    # @brief Create Finance instances for each day where there 
    # was an order
    #
    # Note that this method calculates the profit for all the days requested.
    @classmethod
    def createAll(cls):
        for date in Order.objects.distinct('date').values('date'):
            fin = cls.create(date['date'])
            fin.getProfit()

    ##
    # @brief Create or fetch a Finance instance for the given day
    #
    # @param date The date to get an instance for
    @classmethod
    def create(cls, date=datetime.date.today()):
        try:
            item = Finance(date=date, revenue=0,expenses=0,profit=0)
            item.save()
            return item
        except:
            return Finance.objects.get(pk=date)

    ## Get a QuerySet of all the orders in the day
    #
    # @return A QuerySet of all the orders
    def getOrders(self):
        return Order.objects.filter(date=self.pk)

    ##
    # @brief Calculate the expenses for the day
    #
    # Calculates the expenses and saves them to the database
    # @return The expenses for the day
    def getExpenses(self):
        invPrice = Sum(ExpressionWrapper(
            F('orderitem__menu_item__ingredients__price'),
            output_field=FloatField()) * 
                              (F('orderitem__menu_item__ingredient__amount') /
                              F('orderitem__menu_item__ingredients__amount_per_unit'))
            )
        
        self.expenses = self.getOrders().aggregate(price=invPrice)['price']
        if self.expenses == None:
            self.expenses = 0.00

        return self.expenses

    ##
    # @brief Calculate the revenue for the day
    #
    # Calculates the revenue and saves them to the database
    # @return The revenue for the day
    def getRevenue(self):
        rev = Sum(ExpressionWrapper(F('orderitem__cost'),
                                                  output_field=FloatField()))
        self.revenue = self.getOrders().aggregate(price=rev)['price']
        if self.revenue == None:
            self.revenue = 0.00

        return self.revenue

    ##
    # @brief Calculate the profit for the day
    #
    # Calculates the profit and saves them to the database.
    # It does this by calculating (and saving) the expenses 
    # and revenue and returning the difference.
    #
    # @return The profit for the day
    def getProfit(self):
        self.getExpenses()
        self.getRevenue()
        
        self.profit = self.revenue - self.expenses

        self.save()

        return self.profit

    ##
    # @brief Return a dictionary of Inventory instances and amount of each used in the day
    #
    # @returns A dictionary relating Inventory items to the amount used that day
    def getInventoryUsage(self):
        inv = dict()
        for order in self.getOrders():
            invSum(inv, order.getInventoryUsage())

        return inv

    class Meta:
        db_table = 'finances'

##
# @brief Return a date +/- a certain number of days
#
# @param day The starting date to add/subtract from
# @param delta The number of days to add or subtract
# @return The date which is day plus delta days
def deltaDate(day, delta):
    return datetime.date.fromordinal(day.toordinal() + int(delta))

##
# @brief A class to provide analytical functions over multiple
# financial days
#
class FinanceView():

    ##
    # @brief Create a FinancialView for the date range given
    #
    # The date range given is inclusive of both the start and the end.
    # The start and end dates don't have to be in the database. As long
    # as the parameters are valid dates, the class will work.
    #
    # If you set the object to have an end date past the current day, 
    # you will have to call updateOrders and updateFinances to update
    # the class' information before rerunning reports and analytics.
    #
    # @param start The start date for the view
    # @param end The end for the view
    def __init__(self, start :datetime.date, end :datetime.date):
        self.start_date = start
        self.end_date = end

        self.orders_set = Order.objects.filter(date__gte=self.start_date, date__lte=self.end_date)
        self.finance_set = Finance.objects.filter(date__gte=self.start_date, date__lte=self.end_date)

    ##
    # @brief Get the set of Order objects for this view
    #
    # @return A QuerySet of Order objects
    def getOrders(self):
        return self.orders_set

    ##
    # @brief Update the set of Order objects and return it
    #
    # @return A QuerySet of Order objects
    def updateOrders(self):
        self.orders_set = Order.objects.filter(date__gte=self.start_date, date__lte=self.end_date)
        return self.orders_set

    ##
    # @brief Return the set of finance objects for this view
    # 
    # @return A QuerySet of Finance objects for the days in view
    def getFinances(self):
        return self.finance_set

    ##
    # @brief Update the set of Finance Objects
    # 
    # @return The updated QuerySet of Finance objects
    def updateFinances(self):
        self.finance_set = Finance.objects.filter(date__gte=self.start_date, date__lte=self.end_date)
        return self.finance_set
    
    ##
    # @brief Get a QuerySet representing the inventory usage for these days
    # 
    # @return A QuerySet of Inventory items used, with a 'stock_used' column appended to it
    def getInventoryUsage(self):
        usage = InventoryUsage.objects.filter(date__gte=self.start_date, date__lte=self.end_date)

        # Get the sum total of each item used
        # Basically equivalent to usage.aggregate(amount=Sum('amount_used'))
        amount_query = usage.filter(item=OuterRef('id')).values('item').annotate(amount=Sum('amount_used')).values('amount')

        return Inventory.objects.filter(id__in=usage.values('item')).annotate(
                stock_used=Subquery(amount_query))
    
    ##
    # @brief Return a QuerySet of the Menu items sold, with a 'sales' column annotated
    # 
    # Items which sold nothing have 'sales' set to 0.
    #
    # @return A QuerySet of Menu items with a new column describing how many were sold
    def salesByItem(self):
        items = OrderItem.objects.filter(order__in=self.orders_set.values('id'))

        sum_query = items.filter(menu_item=OuterRef('id')).order_by().annotate(num=Value(1)).values('num').annotate(total=Sum('num', default=0)).values('total')

        return Menu.objects.annotate(sales=Subquery(sum_query)).order_by('-sales')

    ##
    # @brief Return the Inventory items which sold less than the given percent of their stock
    #
    # @param pct The percent threshold for Inventory items. Should be in the range 0 < pct < 1.
    # @return A QuerySet of Inventory items with an annotated column ('percent_usage') indicating the percentage used.
    def excessReport(self, pct):
        usage = self.getInventoryUsage()
        
        return usage.annotate(percent_usage=F('stock_used') / (F('stock')+F('stock_used'))).filter(percent_usage__lte=pct).order_by('-percent_usage') 

    ##
    # @brief Return all Inventory items which have less than min_units*amount_per_unit stock
    #
    # @param The minimum amount of units of product required to have in stock
    # @return A QuerySet of Inventory Items with an annotated column ('num_units') indicating the number of units in stock
    def restockReport(self, min_units=100):
        
        return Inventory.objects.annotate(num_units=F('stock') / F('amount_per_unit')).filter(num_units__lt=min_units)


    ##
    # @brief Return a QuerySet of SalesPair rows, each of which describes a pair of items 
    # that sell together and how many times they sold together. 
    # 
    # The date in these objects is meaningless. The user should interpret the report as
    # being the sum of all of the sold object pairs in the date interval given.
    #
    # Note that the queryset returned by this has some restrictions, such as being unable
    # to be ordered using `.order_by()`.
    #
    # @returns A QuerySet describing how frequently pairs of items sold together
    def sellsTogetherReport(self):

        qset = SalesPair.objects.filter(
            date__gte=self.start_date, 
            date__lte=self.end_date).distinct('item_a', 'item_b').annotate(
            total=Subquery(
                SalesPair.objects.filter(
                    item_a=OuterRef('item_a'), 
                    item_b=OuterRef('item_b'),
                    date__gte=self.start_date,
                    date__lte=self.end_date,
                    ).values('item_a','item_b').annotate(total=Sum('amount')).values('total')
                )
            )

        return qset

    ##
    # @brief Returns the sellsTogetherReport, but as a Python list sorted by the total 
    # amount of each pair sold. 
    #
    # By default the list is sorted in descending order on the column total.
    #
    # @param descending Whether to sort in descending (True) or ascending (False) order
    # @param col The name of table column to sort on
    # @param disp A python function taking a single SalesPair and returning the value
    # @param limit The maximum number of objects to get
    # to return in the sorted list. Basically your __repr__ function
    def sellsTogetherReportSorted(self, descending=True, col='total', disp=lambda x: x, limit=100):
        totals = list(self.sellsTogetherReport().all())
        totals.sort(key=lambda x: eval(f"{-1.0 if descending else 1.0}*x.{col}"))
        return [disp(x) for x in totals[:limit]]
##
# @brief Model to track the usage of Inventory items per day
#
class InventoryUsage(Model):
    
    id = BigAutoField(primary_key=True)

    ## Date that the usage represents
    date = DateField()

    ## Inventory item that the usage represents
    item = ForeignKey('Inventory', on_delete=DO_NOTHING)
    
    ## Amount of the item used in the day
    amount_used  = FloatField()

    ##
    # @brief Get or Create an InventoryUsage row
    # 
    # If the requested row does not exist, it is created with the given
    # information and 0 amount_used. Otherwise, it is returned
    #
    # @param date The date to track the Inventory for
    # @param item The Inventory item that is being tracked
    # @return The InventoryUsage item fetched or created
    @classmethod
    def createOrGet(cls, date, item):
        inv = cls.objects.filter(date=date, item=item)
        if inv.exists():
            return inv.first()

        obj = cls(date=date, item=item, amount_used=0.0)
        obj.save()
        return obj


    def __str__(self):
        return f"Usage of {self.item.name} on date {self.date} : {self.amount_used}"
    

    class Meta:
        ## Constraint that dates and items must be unique
        constraints = [
            UniqueConstraint(fields=['date','item'], name='usage_unique')
        ]

##
# @brief This Model facilitates the creation of the SellsTogetherReport.
#
# This model aggregates the amount sold of every pair of Menu items for each
# day. This makes aggregating the SellsTogetherReport easy, at the expense of
# slightly slowing down the checkout time for each order and taking marginally
# more space on the DB.
class SalesPair(Model):
    ## The ID for an instance
    id = BigAutoField(primary_key=True)

    ## The date that this instance is describing
    date = DateField()

    # The two items (item_a and item_b) are "sorted" by the item they contain's 
    # primary keys. This allows easy fetching of objects using min and max

    ## The item with the smaller primary key
    item_a = ForeignKey('Menu', on_delete=CASCADE, related_name='item_a')
    item_a_name = TextField()

    ## The item with the larger primary key
    item_b = ForeignKey('Menu', on_delete=CASCADE, related_name='item_b')
    item_b_name = TextField()

    ## How frequently the pair were sold together
    amount = IntegerField()

    ##
    # @brief Fetch the corresponding SalesPair object, or create it if it doesn't exist.
    #
    # @param date The date to search for
    # @param i1 One of the item pair. Doesn't have to be largest or smallest pk
    # @param i2 The other item in the pair. Also doesn't have to be largest or smallest
    # @return A SalesPair object. Either a new one if the pair doesn't exist, or the 
    # corresponding one, if it exists.
    @classmethod 
    def getOrCreate(cls, date, i1, i2):
        min_obj = min(i1, i2, key=lambda x: x.pk)
        max_obj = max(i1, i2, key=lambda x: x.pk)
        objs = cls.objects.filter(date=date, item_a_name=min_obj.name, item_b_name=max_obj.name)

        if objs.exists():
            return objs.first()
        else:
            obj = cls(date=date, 
                      item_a=min_obj.pk,
                      item_a_name=min_obj.name,
                      item_b=max_obj.pk,
                      item_b_name=max_obj.name,
                      amount=0)
            obj.save()
            return obj


    class Meta:
        ## The Constraint that dates, item_a, and item_b must be unique for each instance
        constraints = [
                UniqueConstraint(fields=['date', 'item_a_name', 'item_b_name'], name='a_b_unique')
            ]

##
# @brief Inventory Model Class
# 
# The inventory model holds information about each ingredient that must be stocked by the 
# store. It contains the price per ordered unit of ingredient, the number of grams in stock,
# the amount of grams per unit purchased, and the name of the ingredient. 
#
class Inventory(Model):
    ## The ID of the item
    id = BigIntegerField(primary_key=True)
    
    ## The name of the item
    name = TextField()

    ## The price for a single unit of restock
    price = DecimalField(max_digits=11, decimal_places=2) # Up to 999,999,999.99

    ## The current amount of grams in stock
    stock = FloatField()

    ## The amount of grams of the item on order
    ordered = FloatField(blank=True, null=False)

    ## The amount of the item that is purchased per unit of restock
    amount_per_unit = FloatField(blank=False, null=False)

    ##
    # @brief Remove the given dictionary of Inventory instances and floats from each instance's stock
    #
    # @param inv A dictionary of [Inventory, float] representing the amount of each item used
    #
    @classmethod
    def removeFromInv(cls, inv):
        objs = list()
        for key in inv:
            objs.append(key)
            key.stock -= inv[key]

        cls.objects.bulk_update(objs, ['stock'])

    ##
    # @brief Create a new Inventory item with the given information
    #
    # @param id The integer ID to give to the item
    # @param name The name of the Inventory item
    # @param price The price per restock
    # @param stock The starting stock of the item
    # @param amount_per_unit The amount of the item purchased per unit of restock
    @classmethod
    def create(cls, id, name, price, stock, amount_per_unit):
        item = cls(id=id, name=name, price=price, stock=stock, ordered=0, amount_per_unit=amount_per_unit)
        item.save()
        return item

    class Meta:
        db_table = 'inventory'
    
    def __str__(self):
        return f"{self.name} x {self.stock}"

## 
# @brief Menu Model Class
# 
# The menu contains every orderable item on the menu, along with it's price, description, and image.
# Along with these user-facing details, the model is also related to the Inventory model through an
# intermediate Ingredient Model. This allows the menu item to contain its own pseudo-recipe.
class Menu(Model):

    ## The ID of the Menu item
    id = BigAutoField(primary_key=True)

    ## The name of the item
    name = TextField()

    ## The price of the item for the customer
    price = DecimalField(max_digits=11, decimal_places=2)

    ## A short description of the item for the customer
    description = TextField(default="Lorem")
    
    ## The Inventory items used to make the Menu item. Related through the Ingredient model
    ingredients = ManyToManyField(Inventory, through='Ingredient')
    
    ## The size of the drink that this Menu item represents
    size = TextField(blank=False, null=False)

    ## The classification of the item
    type = TextField()
    
    ## The path to the image asset for this Menu item
    image = TextField(null=True)

    ##
    # @brief Gets all the sizes possible for this specific drink
    #
    # @returns A list of 2-tuples of the Menu item ids and sizes
    def getPossibleSizes(self):
        result = list()
        for item in Menu.objects.filter(name=self.name):
            result.append((item.size, item.size))

        return result

    ##
    # @brief Create a new Menu item
    #
    # @param name The name of the new item
    # @param size The size of the new item
    # @param type The type classification of the new item
    # @param image The path to the image asset for the item
    # @return An instance of the new Menu item
    @classmethod
    def create(cls, name, price, size, type, image):
        item = cls(name=str(name), price=float(price), size=str(size), type=str(type), image=image)
        item.save()
        return item
    
    ##
    # @brief Adds the given amount of the given Inventory item as an Ingredient. 
    # 
    # If the Inventory item already exists as an Ingredient, this adds the given
    # amount to the Ingredient.
    #
    # @param ingredient The Inventory item to add
    # @param amount The amount in grams of the item to add
    #
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

    ##
    # @brief Return the amount of the given Inventory item in the Menu item
    #
    # @param ingredient The Inventory item to return the amount of
    # @return The amount of the requested Inventory item
    def getIngredientAmount(self, ingredient: Inventory) -> float:
        return self.ingredient_set.get(inventory=ingredient).amount

    ##
    # @brief Get the price of this Menu item to restock
    # 
    # @returns The price of the ingredients for one of the Menu item
    def getInventoryPrice(self) -> float:
        price_aggregator = Sum(
                    ExpressionWrapper(F('inventory__price'),
                                             output_field=FloatField()) *
                    (F('amount') / F('inventory__amount_per_unit'))
                )
        return self.ingredient_set.aggregate(val=price_aggregator)['val']

    ##
    # @brief Remove the Menu item from the Inventory stock
    #
    #
    def removeFromInventory(self):
        amount_query = self.ingredient_set.filter(inventory=OuterRef('id'))
        Inventory.objects.filter(id__in=self.ingredient_set.values('inventory')).update(
                stock=F('stock')-Subquery(amount_query.values('amount'))
                )
        
    ##
    # @brief Return the amount of each ingredient used in the Menu item
    #
    # @returns A dictionary of Inventory item ids and float amounts of the item used
    def getInventoryUsage(self) :
        return dict(self.ingredient_set.all().values_list('inventory', 'amount'))

    class Meta:
        db_table = 'menu'

    def __str__(self):
        return f"{self.id} : {self.size} {self.name}"

## 
# @brief Ingredient Model Class
# 
# The Ingredient Model is an intermediate model between the Menu and the Inventory. It
# contains a menu item, an inventory item which is an ingredient for the menu item, and 
# a float which represents how many grams of the inventory item are required for the menu 
# item to be made. 
class Ingredient(Model):

    ## The ID of the Ingredient
    id = BigAutoField(primary_key=True)

    # Models Involved in this Ingredient
    ## The Menu item that this Ingredient is for
    menu_item = ForeignKey(Menu, on_delete=CASCADE)

    ## The Inventory item that this Ingredient represents
    inventory = ForeignKey(Inventory, on_delete=CASCADE)

    ## The amount of the Inventory item used
    amount = FloatField()

    ## 
    # @brief Get the price of the Ingredient in the inventory
    # @returns The price to restock one ingredient
    def getPrice(self) -> float:
        return round(float(self.inventory.price) * (self.amount / self.inventory.amount_per_unit),2)

    def __str__(self):
        return f"{self.menu_item.name} :> {self.inventory.name} x {self.amount}"

    class Meta:
        ## The constraint that menu items can only have one of each type of ingredient
        constraints = [
            UniqueConstraint(fields=['menu_item', 'inventory'], name='unique_ingredients')
            ]

## 
# @brief OrderItem Model Class
# 
# An OrderItem is a single menu item which belongs to an order. The OrderItem may have 
# as many customizations added to it as the customer wants, and as many as desired can
# be ordered. 
# 
# The model is related to the Menu Model, the Order Model, and the Customizations Model.
# The model uses an intermediate ItemCustomization model to handle the customizations for
# each item.
class OrderItem(Model):
    ## The ID of the OrderItem
    id = BigAutoField(primary_key=True)

    ## The Order this item belongs to
    order = ForeignKey('Order', on_delete=CASCADE, null=False)

    ## Menu Item that this item represents
    menu_item = ForeignKey(Menu, on_delete=DO_NOTHING, null=False) 

    ## Customization objects added to the item
    customizations = ManyToManyField(Customization, through='ItemCustomization') 

    ## Amount of item requested
    amount = IntegerField(blank=False, null=False)

    ## Price paid by the customer
    cost = DecimalField(max_digits=11, decimal_places=2)

    ##
    # @brief Get list of the different sizes available for the current Menu item
    # 
    # @returns a list of 2-tuples of the Menu item's ID and the size
    def getPossibleSizes(self):
        result = list()
        for item in Menu.objects.filter(name=self.menu_item.name):
            result.append((item.pk, item.size))

        return result

    ##
    # @brief Create a new OrderItem
    #
    # @param order The Order item that this will belong to
    # @param menu_item The Menu item that the OrderItem will contain
    # @param amount The amount of the Menu item that is desired
    # @return The created OrderItem
    @classmethod
    def create(cls,menu_item, amount=1):
        item = cls(menu_item=menu_item, amount=amount)
        item.cost = menu_item.price * amount
        item.save()
        return item

    def addOrder(self,order):
        self.order = order
        self.save()
        return
    ##
    # @brief Get the price of the item and customizations in the inventory
    #
    # @returns The price to restock after the OrderItem is purchased
    def getInventoryPrice(self) -> float:
        custPrice = 0.0
        for cust in self.customizations.all():
            custPrice += cust.getInventoryPrice() 

        return self.amount * (self.menu_item.getInventoryPrice() + custPrice)

    ##
    # @brief Get the usage of each Inventory item in the OrderItem
    # 
    # @return A dictionary of Inventory items and the amount of the item used
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

    ##
    # @brief Get a querySet of Inventory items annotated with a 'stock_used' column
    #
    # @returns The unevaluated QuerySet
    def getInventoryUsageQuerySet(self):
        oi_item = self
        # Get the inventory usage QuerySet of a single Menu Item
        # Usage is labeled 'stock_used'
        m_item = oi_item.menu_item 
        menu_usage = Inventory.objects.filter(
                id__in=m_item.ingredient_set.values('inventory')).annotate(
                stock_used=Subquery(m_item.ingredient_set.filter(
                    inventory=OuterRef('id')).values('amount'))
                )

        # Get the inventory usage QuerySet of a single Customization
        an_set = oi_item.itemcustomization_set.annotate( #Get an annotated set of the ingredient usage 
            ingredient=F('customization__ingredient'),
                      stock_used=F('customization__amount')*F('amount'))

        # QuerySet of Inventory with stock_used annotated with Ingredients used for
        # customizations
        cust_usage = Inventory.objects.filter(id__in=an_set.values('ingredient')).annotate(
                stock_used=Subquery(an_set.filter(
                        ingredient=OuterRef('id')
                    ).values('ingredient').annotate(
                        total=Sum('stock_used')).values('total')
                    )
                )
        
        full_usage = Inventory.objects.filter(
                Q(id__in=cust_usage.values('id')) |
                Q(id__in=menu_usage.values('id'))
            ).annotate(
                    stock_used = 
                    Case(
                        When(id__in=menu_usage.values('id'), 
                             then=Subquery(menu_usage.filter(id=OuterRef('id'))
                                           .values('stock_used'))
                             ),
                        default = 0.0) +
                    Case(
                        When(id__in=cust_usage.values('id'), 
                             then=Subquery(cust_usage.filter(id=OuterRef('id'))
                                           .values('stock_used'))
                             ),
                        default = 0.0))
                    

        return full_usage

    ##
    # @brief Returns a list of the prices of each customization applied
    #
    # @return A dictionary with each ItemCustomization applied and the cost 
    # of the customization
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


    ##
    # @brief Get the total price of all the customizations
    #
    # @returns The total price of all the customizations
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

    ##
    # @brief Because the cost is a function of the customizations applied, this retrieves
    # the cost to the customer
    #
    # @returns The cost to the customer
    def getPrice(self) -> float:
        return round(float(self.cost),2)
    
    ##
    # @brief Force a recalculation of the item's price and return it.
    # 
    # @return The item's calculated price
    def calcPrice(self) -> float:
        self.cost = self.amount * (self.getCustomizationPrice() + float(self.menu_item.price))
        self.save()
        return self.getPrice()

    ##
    # @brief Add the given amount of the given Customization
    #
    # @param cust The Customization to add
    # @param amount The amount of the customization to add
    def addCustomization(self, cust :Customization, amount :float):
        if self.itemcustomization_set.filter(customization=cust).count() > 0:
            self.itemcustomization_set.filter(customization=cust).update(amount=F('amount') + amount)
        else:
            newCust = ItemCustomization(order_item=self, customization=cust, amount=amount)
            newCust.save()

        self.cost = self.amount * (self.getCustomizationPrice() + float(self.menu_item.price))
        self.save()
        return

    ##
    # @brief Add one of each customization in custs 
    #
    # This method is significantly faster than using multiple addCustomization
    # calls because it performs only 2 SQL queries, no matter how many customizations
    # are given. This is at worst equal to addCustomization in efficiency
    # @param custs A list (or other iterable) of Customization objects or primary keys
    def addCustomizations(self, custs):
        cust_items = [ ItemCustomization(order_item=self, customization=pair, amount=0) for pair in custs]
        
        self.itemcustomization_set.filter(customization__in=custs).update(amount=F('amount')+Value(1))
        ItemCustomization.objects.bulk_create(cust_items, ignore_conflicts=True)

        self.cost = self.amount * (self.getCustomizationPrice() + float(self.menu_item.price))
        self.save()




    class Meta:
        db_table = 'order_items'
        
    def __str__(self):
        return f"{self.menu_item} : {self.amount}"

## 
# @brief ItemCustomization Model Class
# 
# The ItemCustomization Model is an intermediate model between an OrderItem and a
# Customization. It contains how much of the customization is to be added to the
# OrderItem. 
class ItemCustomization(Model):

    ## The ID of the ItemCustomization
    id = BigAutoField(primary_key=True)
    
    ## The OrderItem associated with this customization
    order_item = ForeignKey(OrderItem, CASCADE)
    
    ## The Customization associated with this
    customization = ForeignKey(Customization, CASCADE)

    ## The amount of the Customization added
    amount = IntegerField(null=False, blank=False)
    
    ## 
    # @brief Get the price to restock after this customization has been ordered
    #
    # @return The price to restock
    def getInventoryPrice(self) -> float:
        return self.customization.getInventoryPrice() * self.amount

    ##
    # @brief Get the price of the customization(s)
    #
    # @return The price of the customization(s)
    def getCustomizationPrice(self) -> float: 
        return round(float(self.customization.cost*self.amount),2)
        
    def __str__(self):
        return f"{self.order_item.menu_item.name} :> {self.customization.name} {self.customization.type} x {self.amount}"
    
    class Meta:

        ## The constraint that orderitems may only have a single row per customization item
        constraints = [
            UniqueConstraint(fields=['order_item', 'customization'], name='itemcustomization_single_cust')
            ]

##
# @brief Order Model Class
# 
# The Order Model allows users to collect multiple menu items, add
# customizations to each item as desired, and then place the order
# by removing the used ingredients from the DB. 
class Order(Model):
    ## ID of the order
    id = BigAutoField(primary_key=True)

    ## Cashier who processed the order
    cashier = TextField(blank=True, null=True)

    ## Date that the order was processed
    date = DateField(blank=True, null=True)

    ## Menu items and Customizations purchased, through the OrderItem model
    items = ManyToManyField(Menu, through='OrderItem')

    ## Cost of the order. Added after checkout
    price = DecimalField(null=True, blank=True, max_digits=11, decimal_places=2);

    ##
    # @brief Get a dictionary of Inventory items and floats which describes the
    # amount of each item used.
    #
    # @returns A dictionary with the Inventory usage for the order
    def getInventoryUsage(self) -> dict[Inventory, float]:
        inv = dict()
        for item in self.orderitem_set.all():
            invSum(inv, item.getInventoryUsage())

        return inv
            
    ##
    # @brief Get the price to restock after this order
    # 
    # @return The price to restock the order
    def getInventoryPrice(self) -> float:
        invPrice = 0.0
        for item in self.orderitem_set.all():
            invPrice += item.getInventoryPrice()
        return invPrice

    ##
    # @brief Get the price of the order and save it
    #
    # @return The price of the order for the customer
    def getPrice(self) -> float:
        self.price = self.calcPrice()
        self.save()
        return round(self.price,2)

    ##
    # @brief Force a recalculation of the price of an order
    #
    # Note that this calls calcPrice() for every OrderItem. This
    # may be a little slow. 
    #
    # @return The calculated the price of the order
    def calcPrice(self) -> float:
        self.price = 0.0
        for item in self.orderitem_set.all():
            self.price += item.calcPrice()
        self.save()
        return round(self.price, 2)

    ## 
    # @brief Get the Inventory usage for the entire order as a
    # QuerySet of the Inventory table with the 'stock_used' column annotated onto it
    def getInventoryUsageQuerySet(self):
        query = Q()
        stmt = Case()
        for index, item in enumerate(self.orderitem_set.all()):
            q = item.getInventoryUsageQuerySet()
            query |= Q(id__in=q.values('id'))

            case_stmt = Case(
                    When(
                        id__in=q.values('id'),
                        then=Subquery(q.filter(id=OuterRef('id')).values('stock_used'))
                        ),
                    default=0.0
                    )

            if index == 0:
                stmt = case_stmt
            else:
                stmt += case_stmt

        return Inventory.objects.filter(query).annotate(stock_used=stmt)
    
    ##
    # @brief Finalize an order by removing its stock from the Inventory
    # and by placing the Inventory used into the InventoryUsage table.
    #
    # This function has a portion which runs in Theta(2^n) time. I've 
    # optimized this as much as possible so that the only section of
    # code which runs in that awful time is a string join and the creation
    # of combinations of sold objects.  
    def checkout(self):
        usage = self.getInventoryUsageQuerySet()

        # Create InventoryUsage items
        usageItems = [InventoryUsage(date=self.date, item=i, amount_used=0.0) for i in usage]

        # Bulk create (or do nothing) the InventoryUsage 
        InventoryUsage.objects.bulk_create(usageItems, ignore_conflicts=True)

        # Update the inventory usage
        InventoryUsage.objects.filter(date=self.date, item__in=usage).update(
                amount_used=F('amount_used') + Subquery(usage.filter(id=OuterRef('item')).values('stock_used'))
                )

        # print("Usage Calculated")
            
        # Update the Inventory stock
        usage.update(stock=F('stock')-F('stock_used'))

        # print("Stock Updated")

        # Add purchased pairs to the SalesPairs table

        sorted_items = self.items.order_by('id').all()
        num_items = self.items.count()
        if num_items < 2:
            return
        combos = list()
        arr = '('

        # Create all combinations of items
        # Also create a string with an SQL array of pairs of Menu items
        for i in range(num_items-1):
            for j in range(i+1,num_items):
                combos.append((sorted_items[i],sorted_items[j]))
                arr += f"({sorted_items[i].pk},{sorted_items[j].pk})"
                if not (i == num_items-2 and j == num_items-1):
                    arr += ','
        arr += ')'

        combonames = list(map(lambda x: list(map(lambda y: y.name, x)), zip(*combos)))

        # Create all SalesPair objects that don't already exist
        SalesPair.objects.bulk_create([SalesPair(date=self.date, item_a_name=p[0].name, item_a=p[0], item_b=p[1], item_b_name=p[1].name, amount=0) for p in combos], ignore_conflicts=True)
        SalesPair.objects.filter(date=self.date, item_a_name__in=combonames[0], item_b_name__in=combonames[1]).update(amount=F('amount')+Value(1))

        ## Raw SQL Update

        # Add 1 to every SalesPair involved in this order
        # with connection.cursor() as cursor:
        #     cursor.execute("UPDATE storefront_salespair SET amount=amount+1 WHERE (item_a_id, item_b_id) IN " + arr)
 
        # print("SalesPairs Added")


    ##
    # @brief Create a new order
    #
    # @param cashier The name of the cashier
    # @param date The date at which the order was placed
    # @return The new Order item created
    @classmethod
    def create(cls, cashier :str, date = datetime.datetime.now()):
        ordr = cls(cashier=cashier, date=date, price=0)
        ordr.save()
        return ordr


    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"{self.date}"

##
# @brief Add two Inventory dictionaries
#
# @param out The dictionary that the result will be saved to
# @param inv The dictionary that will be added to out
def invSum(out :dict[Inventory,float], inv :dict[Inventory, float]):

    for key in inv:
        if key in out:
            out[key] += inv[key]
        else:
            out[key] = inv[key]
