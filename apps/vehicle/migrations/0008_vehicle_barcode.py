# Generated by Django 4.0.6 on 2022-07-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0007_vehicle_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='barcode',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
