# Generated by Django 4.2.6 on 2023-11-14 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_project_unique_together'),
        ('enrollments', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tasksolution',
            unique_together={('enrollment', 'task')},
        ),
    ]
