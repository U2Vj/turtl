# Generated by Django 4.1.7 on 2023-02-16 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
