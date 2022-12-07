from django.db.models import *
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
# @brief A class to provide analytics functions over multiple
# financial days
#
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
    # information. Otherwise, the row's amount used is increased by the 
    # given amount
    #
    # @param date The date to track the Inventory for
    # @param item The Inventory item that is being tracked
    # @param amount_used The amount of the item that was used in grams
    # @return The InventoryUsage item fetched or created
    @classmethod
    def create(cls, date, item, amount_used):
        try:
            inv = cls(date=date, item=item, amount_used=amount_used)
            inv.save()
            return inv
        except:
            inv = cls.objects.get(date=date)
            inv.amount_used += amount_used
            inv.save()
            return inv

    def __str__(self):
        return f"Usage of {self.item.name} on date {self.date} : {self.amount_used}"

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
            result.append((item.pk, item.size))

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
    def create(cls, order, menu_item, amount=1):
        item = cls(order=order, menu_item=menu_item, amount=amount)
        item.cost = menu_item.price * amount
        item.save()
        return item

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
                stock_used=(Subquery(m_item.ingredient_set.filter(
                    inventory=OuterRef('id')).values('amount')))
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
                    ).values('stock_used'))
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
        return float(self.cost)

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
        return

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
        return round(float(cust.cost*cust.amount),2)
        

    def __str__(self):
        return f"{self.order_item.menu_item.name} :> {self.customization.name} {self.customization.type} x {self.amount}"

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
        price = 0.0
        for item in self.orderitem_set.all():
            price += item.getPrice()

        self.price = price
        return round(price,2)

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
    def checkout(self):
        usage = self.getInventoryUsageQuerySet()
        for inv in usage:
            # Save the used stock for the day's count
            InventoryUsage.create(self.date, inv, inv.stock_used)
            
        # Update the Inventory stock
        usage.update(stock=F('stock')-F('stock_used'))


    ##
    # @brief Create a new order
    #
    # @param cashier The name of the cashier
    # @param date The date at which the order was placed
    # @return The new Order item created
    @classmethod
    def create(cls, cashier :str, date = datetime.datetime.now()):
        ordr = cls(cashier=cashier, date=date)
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
