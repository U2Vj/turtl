# Generated by Django 3.0.7 on 2023-09-18 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20230901_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMINISTRATOR', 'Administrator'), ('INSTRUCTOR', 'Instructor'), ('STUDENT', 'Student')], default='STUDENT', max_length=13),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=128, null=True),
        ),
    ]