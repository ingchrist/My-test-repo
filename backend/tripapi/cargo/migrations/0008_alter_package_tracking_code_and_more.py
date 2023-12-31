# Generated by Django 4.0 on 2023-02-23 20:41

from django.db import migrations
import utils.base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0007_alter_order_tracking_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='tracking_code',
            field=utils.base.fields.TrackingCodeField(max_length=60, prefix='PKG'),
        ),
        migrations.AlterField(
            model_name='pricepackage',
            name='tracking_code',
            field=utils.base.fields.TrackingCodeField(max_length=60, prefix='LGS-PRC'),
        ),
    ]
