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

# Repopulation Variables. Set these to True to repopulate the corresponding table
inventory_repopulate = False # Set to true to modify the inventory table
inventory_append = False # Set to true to append items to the inventory.

menu_repopulate = False # Set to true to modify the menu table
menu_append = False  # Set to true to append data to the menu instead of clearing it

# Repopulation Files. Set these to the path to the TSV file with the data
inventory_file = '../Inventory.tsv'
menu_file = '../Menu.tsv'

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
### Expected TSV header: id, name, price, ingredients, size, type

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

            item = Menu.create(name, price, size, type)

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

