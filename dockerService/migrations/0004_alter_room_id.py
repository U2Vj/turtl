# Generated by Django 4.2.6 on 2023-10-12 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dockerService', '0003_auto_20230901_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
