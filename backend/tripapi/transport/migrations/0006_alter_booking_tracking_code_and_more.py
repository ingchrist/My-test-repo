# Generated by Django 4.0 on 2022-09-15 13:57

from django.db import migrations
import utils.base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0005_alter_booking_created_alter_review_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='tracking_code',
            field=utils.base.fields.TrackingCodeField(),
        ),
        migrations.AlterField(
            model_name='driver',
            name='tracking_code',
            field=utils.base.fields.TrackingCodeField(),
        ),
        migrations.AlterField(
            model_name='tripobject',
            name='tracking_code',
            field=utils.base.fields.TrackingCodeField(),
        ),
        migrations.AlterField(
            model_name='tripplan',
            name='tracking_code',
            field=utils.base.fields.TrackingCodeField(),
        ),
    ]
