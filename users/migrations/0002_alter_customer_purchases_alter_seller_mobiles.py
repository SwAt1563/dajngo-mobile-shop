# Generated by Django 4.0.6 on 2022-07-28 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='purchases',
            field=models.ManyToManyField(blank=True, default=None, to='products.mobile'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='mobiles',
            field=models.ManyToManyField(blank=True, default=None, to='products.mobile'),
        ),
    ]