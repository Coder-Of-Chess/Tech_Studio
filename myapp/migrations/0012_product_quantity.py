# Generated by Django 4.1.5 on 2023-02-02 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0011_rename_status_producttransaction_payment_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="quantity",
            field=models.IntegerField(default=40),
            preserve_default=False,
        ),
    ]
