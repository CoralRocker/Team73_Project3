# Generated by Django 4.1.2 on 2022-11-08 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storefront", "0004_alter_menu_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="menu",
            name="image_asset",
            field=models.FilePathField(default=""),
            preserve_default=False,
        ),
    ]
