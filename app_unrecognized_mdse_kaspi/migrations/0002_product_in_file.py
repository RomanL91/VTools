# Generated by Django 5.1.5 on 2025-01-22 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_unrecognized_mdse_kaspi", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="in_file",
            field=models.BooleanField(default=True),
        ),
    ]
