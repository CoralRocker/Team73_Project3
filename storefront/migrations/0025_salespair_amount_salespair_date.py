# Generated by Django 4.1.3 on 2022-12-09 02:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storefront", "0024_salespair_salespair_a_b_unique"),
    ]

    operations = [
        migrations.AddField(
            model_name="salespair",
            name="amount",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="salespair",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2022, 12, 9, 2, 10, 15, 374862, tzinfo=datetime.timezone.utc
                )
            ),
            preserve_default=False,
        ),
    ]
