# Generated by Django 4.1.2 on 2022-11-22 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("storefront", "0011_alter_orderitem_menu_item"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="finance",
            name="orders",
        ),
    ]