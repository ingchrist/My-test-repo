# Generated by Django 4.0 on 2022-09-12 14:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.base.validators


class Migration(migrations.Migration):

    replaces = [('cargo', '0001_initial'), ('cargo', '0002_package_price_packages'), ('cargo', '0003_package_tracking_code'), ('cargo', '0004_pricepackage_tracking_code'), ('cargo', '0005_alter_pricepackage_tracking_code'), ('cargo', '0006_alter_pricepackage_tracking_code'), ('cargo', '0007_auto_20220501_2351'), ('cargo', '0008_auto_20220502_1021'), ('cargo', '0009_alter_order_status'), ('cargo', '0010_auto_20220502_1411'), ('cargo', '0011_alter_order_status'), ('cargo', '0012_logistic_slug_name_alter_logistic_name_and_more'), ('cargo', '0013_alter_order_tracking_code_and_more'), ('cargo', '0014_alter_order_tracking_code_and_more'), ('cargo', '0015_remove_order_transaction')]

    initial = True

    dependencies = [
        ('payment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Logistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, validators=[utils.base.validators.validate_special_char])),
                ('rating', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('slug_name', models.SlugField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('status', models.CharField(choices=[('pickup', 'Pickup'), ('in_warehouse', 'In warehouse'), ('in_transit', 'In transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], max_length=25)),
                ('tracking_code', models.CharField(max_length=20, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('logistic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargo.logistic')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0, validators=[utils.base.validators.validate_rating_level])),
                ('comment', models.TextField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargo.order')),
            ],
            options={
                'verbose_name': 'Logistic review',
            },
        ),
        migrations.CreateModel(
            name='PricePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_location', models.CharField(help_text='Location where goods will shipped from', max_length=255)),
                ('to_location', models.CharField(help_text='Location where goods will shipped to', max_length=255)),
                ('price', models.FloatField(help_text='Price per 0.5kg for the goods to be shipped')),
                ('logistic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargo.logistic')),
                ('tracking_code', models.CharField(editable=False, max_length=50, unique=True)),
                ('delivery_date', models.IntegerField(default=2, help_text='The amount of days after pickup to delivery')),
                ('pickup_time', models.IntegerField(default=0, help_text='Amount of days to pickup from payment day.\n        e.g if you input 2, that means you will pickup on the\n        second day after payment day.')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Package Shipping Price',
                'ordering': ('-price',),
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, validators=[utils.base.validators.validate_special_char])),
                ('phone', models.CharField(max_length=17, validators=[utils.base.validators.validate_phone])),
                ('email', models.EmailField(max_length=254)),
                ('receiver_name', models.CharField(max_length=40, validators=[utils.base.validators.validate_special_char])),
                ('receiver_phone', models.CharField(max_length=17, validators=[utils.base.validators.validate_phone])),
                ('receiver_email', models.EmailField(max_length=254)),
                ('cargo', models.CharField(choices=[('parcel', 'Parcel')], max_length=20)),
                ('cargo_name', models.CharField(max_length=100)),
                ('quantity', models.FloatField(default=0.0)),
                ('weight', models.FloatField(default=0.0)),
                ('pickup', models.CharField(max_length=200)),
                ('delivery', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('price_packages', models.ManyToManyField(to='cargo.PricePackage')),
                ('tracking_code', models.CharField(editable=False, max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='package',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cargo.package'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pickup_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('pickup', 'Pickup'), ('in_warehouse', 'In warehouse'), ('in_transit', 'In transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], max_length=25),
        ),
        migrations.RemoveField(
            model_name='order',
            name='logistic',
        ),
        migrations.AddField(
            model_name='order',
            name='logistic_package',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.PROTECT, to='cargo.pricepackage'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('unpicked', 'Unpicked'), ('pickup', 'Pickup'), ('in_warehouse', 'In warehouse'), ('in_transit', 'In transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], max_length=25),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_code',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_code',
            field=models.CharField(editable=False, max_length=50, unique=True),
        ),
    ]
