# Generated by Django 4.1.2 on 2022-11-08 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customization",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("cost", models.DecimalField(decimal_places=2, max_digits=11)),
                ("type", models.TextField()),
                ("amount", models.FloatField()),
                ("name", models.TextField()),
            ],
            options={
                "db_table": "customizations",
            },
        ),
        migrations.CreateModel(
            name="Finance",
            fields=[
                ("date", models.DateField(primary_key=True, serialize=False)),
                ("orders", models.TextField()),
                ("revenue", models.DecimalField(decimal_places=2, max_digits=11)),
                ("expenses", models.DecimalField(decimal_places=2, max_digits=11)),
                ("profit", models.DecimalField(decimal_places=2, max_digits=11)),
                ("inventory_usage", models.TextField()),
            ],
            options={
                "db_table": "finances",
            },
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("amount", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Inventory",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("name", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=11)),
                ("stock", models.FloatField()),
                ("ordered", models.FloatField(blank=True)),
                ("amount_per_unit", models.FloatField()),
            ],
            options={
                "db_table": "inventory",
            },
        ),
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=11)),
                ("size", models.TextField()),
                ("type", models.TextField()),
                (
                    "ingredients",
                    models.ManyToManyField(
                        through="storefront.Ingredient", to="storefront.inventory"
                    ),
                ),
            ],
            options={
                "db_table": "menu",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("cashier", models.TextField(blank=True, null=True)),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=11, null=True
                    ),
                ),
            ],
            options={
                "db_table": "orders",
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("amount", models.IntegerField()),
                (
                    "customizations",
                    models.ManyToManyField(to="storefront.customization"),
                ),
                (
                    "menu_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="storefront.menu",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="storefront.order",
                    ),
                ),
            ],
            options={
                "db_table": "order_items",
            },
        ),
        migrations.AddField(
            model_name="ingredient",
            name="inventory",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="storefront.inventory"
            ),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="menu_item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="storefront.menu"
            ),
        ),
        migrations.AddField(
            model_name="customization",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="storefront.inventory"
            ),
        ),
    ]
