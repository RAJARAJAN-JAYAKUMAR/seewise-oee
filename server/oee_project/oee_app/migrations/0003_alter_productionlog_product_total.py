# Generated by Django 5.0.6 on 2024-06-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oee_app', '0002_productionlog_product_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionlog',
            name='product_total',
            field=models.IntegerField(),
        ),
    ]