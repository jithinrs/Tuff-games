# Generated by Django 4.1 on 2022-10-11 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_categoryoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='catoffer', to='products.categories'),
        ),
    ]