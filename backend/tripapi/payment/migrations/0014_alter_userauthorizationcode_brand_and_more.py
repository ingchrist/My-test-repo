# Generated by Django 4.0 on 2023-02-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_alter_transaction_bank_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userauthorizationcode',
            name='brand',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userauthorizationcode',
            name='channel',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userauthorizationcode',
            name='country_code',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
