# Generated by Django 5.0.6 on 2024-06-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0004_reservation_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalpost',
            name='is_vacant',
            field=models.BooleanField(default=True),
        ),
    ]
