# Generated by Django 4.0 on 2023-09-16 13:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0014_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='weight',
            field=models.FloatField(default=0.0, help_text='Weight in kg', validators=[django.core.validators.MinValueValidator(0.5, message='Weight must be greater than 0.5kg')]),
        ),
    ]
