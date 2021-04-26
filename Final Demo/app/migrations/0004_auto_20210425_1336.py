# Generated by Django 3.1.5 on 2021-04-25 18:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210425_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='zipcode',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(999999999)]),
        ),
    ]