# Generated by Django 4.0 on 2022-06-27 18:55

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_remove_bankaccount_tracking_code_bankaccount_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='transaction',
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='total_revenue',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='payment',
            name='bank_account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='payment.bankaccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 27, 18, 54, 39, 655282, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='payment.payment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created',
            field=models.DateTimeField(editable=False),
        ),
    ]
