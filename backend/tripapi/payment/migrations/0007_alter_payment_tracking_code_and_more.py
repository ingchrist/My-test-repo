# Generated by Django 4.0 on 2022-06-28 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_remove_payment_category_alter_payment_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='tracking_code',
            field=models.CharField(editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tracking_code',
            field=models.CharField(editable=False, max_length=50, unique=True),
        ),
    ]
