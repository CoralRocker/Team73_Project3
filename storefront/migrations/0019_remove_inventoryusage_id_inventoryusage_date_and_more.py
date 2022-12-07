# Generated by Django 4.1.3 on 2022-12-06 16:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storefront", "0018_alter_inventoryusage_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inventoryusage",
            name="id",
        ),
        migrations.AddField(
            model_name="inventoryusage",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2022, 12, 6, 16, 39, 3, 425711, tzinfo=datetime.timezone.utc
                ),
                primary_key=True,
                serialize=False,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=11),
            preserve_default=False,
        ),
    ]