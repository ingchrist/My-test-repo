# Generated by Django 4.0 on 2023-09-16 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0013_alter_package_cargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('unpicked', 'Unpicked'), ('pickup', 'Pickup'), ('in_warehouse', 'In warehouse'), ('in_transit', 'In transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='unpicked', max_length=25),
        ),
    ]
