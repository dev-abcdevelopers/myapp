# Generated by Django 5.0.4 on 2024-04-22 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_apiaccesslog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiaccesslog',
            name='api_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.userapikey'),
        ),
    ]