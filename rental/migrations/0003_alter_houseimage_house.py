# Generated by Django 5.0.6 on 2024-05-28 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseimage',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='rental.house'),
        ),
    ]
