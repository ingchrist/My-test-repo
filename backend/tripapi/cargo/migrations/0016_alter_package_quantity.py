# Generated by Django 4.0 on 2023-09-16 13:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0015_alter_package_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Quantity must be greater than 0')]),
        ),
    ]
