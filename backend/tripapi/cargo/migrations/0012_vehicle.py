# Generated by Django 4.0 on 2023-06-15 11:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.base.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0011_logistic_logistics_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[utils.base.validators.validate_special_char])),
                ('kind', models.CharField(choices=[('bike', 'Bike'), ('bus', 'Bus'), ('train', 'Train'), ('plane', 'Plane')], max_length=20)),
                ('tag', models.SlugField(unique=True)),
                ('plate_number', models.CharField(error_messages={'unique': 'Plate number has already been used by another vehicle'}, max_length=20, unique=True)),
                ('capacity', models.PositiveSmallIntegerField(default=1, help_text='Amount of passengers that can be in vehicle', validators=[django.core.validators.MaxValueValidator(500)])),
                ('active', models.BooleanField(default=False)),
                ('send_mail_verification', models.BooleanField(default=False)),
                ('logistic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargo.logistic')),
            ],
        ),
    ]