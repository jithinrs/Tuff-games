# Generated by Django 4.1 on 2022-10-28 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0042_alter_categories_category_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_max_price',
            field=models.IntegerField(max_length=255),
        ),
    ]