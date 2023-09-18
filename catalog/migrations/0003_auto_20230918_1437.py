# Generated by Django 3.0.7 on 2023-09-18 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0002_auto_20230901_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassroomTemplateInstructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classroomtemplateinstructor_set_added_by', to=settings.AUTH_USER_MODEL)),
                ('classroom_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ClassroomTemplate')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroomtemplateinstructor_set_instructor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ClassroomTemplateManager',
        ),
        migrations.AddField(
            model_name='classroomtemplate',
            name='instructors',
            field=models.ManyToManyField(related_name='classroom_templates', through='catalog.ClassroomTemplateInstructor', to=settings.AUTH_USER_MODEL),
        ),
    ]
