# Generated by Django 5.0.6 on 2024-06-03 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0010_reservation_refund_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='price',
            field=models.DecimalField(decimal_places=0, default=3000000, max_digits=10),
        ),
    ]
