# Generated by Django 4.1.2 on 2022-11-22 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("storefront", "0012_remove_finance_orders"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="finance",
            name="inventory_usage",
        ),
    ]