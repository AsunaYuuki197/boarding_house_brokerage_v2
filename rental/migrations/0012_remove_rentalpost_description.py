# Generated by Django 5.0.6 on 2024-06-04 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0011_alter_house_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalpost',
            name='description',
        ),
    ]