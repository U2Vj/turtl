# Generated by Django 4.2.6 on 2023-11-05 20:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0003_add_test_data'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='classroominstructor',
            unique_together={('classroom', 'instructor')},
        ),
    ]