# Generated by Django 5.0.7 on 2024-07-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bridge',
            name='location',
            field=models.CharField(max_length=100),
        ),
    ]
