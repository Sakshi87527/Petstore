# Generated by Django 4.2.7 on 2024-01-08 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0004_cart'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cart',
            table='cart',
        ),
        migrations.AlterModelTable(
            name='customer',
            table='customer',
        ),
    ]
