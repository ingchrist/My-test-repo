# Generated by Django 4.0 on 2022-09-12 13:29

from django.db import migrations, models
import django.db.models.deletion
import utils.base.general


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_squashed_0012_remove_booking_payment_remove_passenger_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='passenger',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transport.passenger'),
        ),
        migrations.AlterField(
            model_name='tripobject',
            name='transporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transport.transporter'),
        ),
        migrations.AlterField(
            model_name='tripplan',
            name='transporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transport.transporter'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='kind',
            field=models.CharField(choices=[('bike', 'Bike'), ('bus', 'Bus'), ('train', 'Train'), ('plane', 'Plane')], max_length=20),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='proof_of_ownership',
            field=models.FileField(upload_to=utils.base.general.vehicle_upload_path),
        ),
    ]
