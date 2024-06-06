# Generated by Django 5.0.6 on 2024-06-01 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0005_rentalpost_is_vacant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalpost',
            name='is_vacant',
        ),
        migrations.AddField(
            model_name='rentalpost',
            name='available_vacancies',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='rentalpost',
            name='total_vacancies',
            field=models.PositiveIntegerField(default=1),
        ),
    ]