# Generated by Django 3.1.5 on 2021-04-25 18:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210324_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelquote',
            name='rate',
            field=models.DecimalField(decimal_places=4, default=1.5, max_digits=10000, verbose_name='Price/Gallon'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='zipcode',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999999)]),
        ),
    ]
