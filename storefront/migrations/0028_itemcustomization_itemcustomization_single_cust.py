# Generated by Django 4.1.3 on 2022-12-11 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storefront", "0027_inventoryusage_usage_unique"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="itemcustomization",
            constraint=models.UniqueConstraint(
                fields=("order_item", "customization"),
                name="itemcustomization_single_cust",
            ),
        ),
    ]
