#####
#
# DATABASE REPOPULATION SCRIPT
# 
# Use this script to add data from TSV files into the DB.
#
#####

### User Variables And Config
###
### modify the variables below to configure what tables will be repopulated
### NOTE: Tables will be wiped before being repopulated unless {table}_append is true

# Randomized Order Creation
import datetime
from dateutil.rrule import DAILY, rrule
create_random_orders = True
start_date = datetime.date(2022, 12, 8)
end_date = datetime.date.today()

min_order_per_day = 0
max_order_per_day = 100

min_item_per_order = 1
max_item_per_order = 30

min_amt_per_item = 1
max_amt_per_item = 5

min_cust_per_item = 0
max_cust_per_item = 5

# Repopulation Variables. Set these to True to repopulate the corresponding table
inventory_repopulate = False # Set to true to modify the inventory table
inventory_append = False # Set to true to append items to the inventory.

menu_repopulate = False # Set to true to modify the menu table
menu_append = False  # Set to true to append data to the menu instead of clearing it

customization_repopulate = False # Set to true to modify the customizations table
customization_append = False # Set to true to append data to the customizations instead of clearing it

# Repopulation Files. Set these to the path to the TSV file with the data
inventory_file = '../Inventory.tsv'
menu_file = '../Menu.tsv'
customizations_file = '../Customizations.tsv'

#####
#
# END OF CONFIGURATION. DO NOT MODIFY ANYTHING PAST THIS POINT!
#
#####

import django
import os
import sys
sys.path.append(os.curdir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()


from storefront.models import *
import re # Regex
import csv # CSV/TSV File parsing
import random

###
### Inventory Repopulation
### 
### Expected TSV header: id, name, price, stock, ordered, unit

if inventory_repopulate:
    if not inventory_append:
        Inventory.objects.all().delete() # Delete all objects
        print("Replacing all Inventory Objects")
    else:
        print("Adding to the Inventory Table")

    with open(inventory_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        next(reader)
        count = 0 
        for row in reader:
            id = int(row[0])
            name = row[1]
            price = float(row[2])
            stock = float(row[3])
            ordered = float(row[4])
            unit = float(row[5])
            
            item = Inventory(id=id, name=name, price=price, stock=stock, ordered=ordered, amount_per_unit=unit)
            item.save()
            print(f"\r\033[2KFinished ID {item.id}", end='')
            count+=1
        print("")
        if inventory_append:
            print(f"Updated table Inventory with {count} new items")
        else:
            print(f"Replaced table Inventory, now has {count} items")

###
### Menu Repopulation
### 
### Expected TSV header: id, name, price, ingredients, size, type, image asset

if menu_repopulate:
    if not menu_append:
        Menu.objects.all().delete() # Delete all objects
        print("Replacing all Menu items")
    else:
        print("Adding to the Menu")

    with open(menu_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        next(reader)
        count = 0
        for row in reader:
            name = row[1]
            price = float(row[2])
            size = row[4]
            type = row[5]
            image = row[6]

            if not os.path.exists(image):
                print(f"\nPath {image} does not exist for item {name}")

            item = Menu.create(name, price, size, type, image)

            for pair in re.findall('(\(\d+,\s*\d+\))', row[3]):
                data = re.findall('\d+', pair)
                inv = int(data[0])
                amount = float(data[1])
                item.addIngredient(Inventory.objects.get(pk=inv), amount)
            
            count+=1
            print(f"\r\033[2KFinished ID {item.id}", end='')
        print("")
        if menu_append:
            print(f"Appended {count} items to Menu")
        else:
            print(f"Replaced Menu with {count} items")


###
### Customizations Repopulation
### 
### Expected TSV header: id, name, price, amount, type, ingredient

if customization_repopulate:
    if not customization_append:
        Customization.objects.all().delete() # Delete objects
        print("Replacing all Customizations")
    else:
        print("Adding to Customizations")

    with open(customizations_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        next(reader) # Skip Header
        count = 0;
        for row in reader:
            name = row[1]
            price = float(row[2])
            amount = float(row[3])
            type = row[4]
            __ing = int(row[5])
            ingredient = Inventory.objects.get(pk=__ing)

            cust = Customization(name=name, cost=price, type=type, amount=amount, ingredient=ingredient)
            cust.save()
            count += 1
            print(f"\r\033[2KFinished ID {cust.id}", end='')
        print("")
        if customization_append:
            print(f"Appended {count} items to Customization")
        else:
            print(f"Replaced Customization with {count} items")


###
### Randomized Order Creation
###


if create_random_orders:
    import itertools

    custs = list(Customization.objects.all())
    items = list(Menu.objects.all())

    for day in rrule(DAILY, dtstart=start_date, until=end_date): 
        num_orders = random.randint(min_order_per_day, max_order_per_day)
        print(f"For day {day}: {num_orders} orders")

        orders = [Order(cashier='randomly generated', date=day.date()) for i in range(num_orders)]
        order_amts = [( # Generate Order Helper Amounts
                num_items, #                                                                            number of items for this order
                random.choices(range(min_amt_per_item, max_amt_per_item+1), k=num_items), #             amt of each orderItem
                random.choices(range(min_cust_per_item, max_cust_per_item+1), k=num_items), #           amount of customizations per item
            ) for o in range(num_orders) if (num_items:=random.randint(min_item_per_order, max_item_per_order)) != None]

        order_menu_cust_items = [(
                [(
                    random.choice(items),                           # Menu item for the OrderItem
                    random.choices(custs, k=order_amts[o][2][i]),   # Customization list
                ) for i in range(order_amts[o][0])]
            ) for o in range(num_orders)]

        order_items = [
                [
                    OrderItem(order=orders[o], menu_item=order_menu_cust_items[o][i][0], amount=order_amts[o][1][i], cost=0.0) # Create the OrderItem
                for i in range(order_amts[o][0])] # Loop through items in order
            for o in range(num_orders)] # Loop through orders

        order_item_customizations = [
                [
                    [
                        ItemCustomization(order_item=order_items[o][i], customization=order_menu_cust_items[o][i][1][c], amount=1) # Create the customization
                    for c in range(order_amts[o][2][i]) ] # Loop through each customization
                for i in range(order_amts[o][0])] # Loop through items in order
            for o in range(num_orders)] # Loop through orders

        orders = Order.objects.bulk_create(orders)

        orderitems_flat = itertools.chain.from_iterable(order_items)
        itemcusts_flat = itertools.chain.from_iterable(itertools.chain.from_iterable(order_item_customizations))

        OrderItem.objects.bulk_create(orderitems_flat)
        ItemCustomization.objects.bulk_create(itemcusts_flat, ignore_conflicts=True)

        print("All orders created. Checking out")
        for i, o in enumerate(orders):
            print(f"Order {i} / {len(orders)}")
            o.checkout()
            print("\033[1F\033[0J", end='')

        print("\033[2F\033[J", end='')
    print("All orders successfully created and checked out")    
