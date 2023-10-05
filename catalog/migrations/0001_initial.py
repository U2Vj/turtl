# Generated by Django 3.0.7 on 2023-09-19 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rules.contrib.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptanceCriteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criteria_type', models.CharField(choices=[('manual', 'Manual'), ('questionnaire', 'Questionnaire'), ('regex', 'Regex'), ('flag', 'Flag')], default='manual', max_length=20)),
                ('regex', models.CharField(blank=True, max_length=200)),
                ('flag', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='catalog.Classroom')),
            ],
            options={
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('question_type', models.CharField(choices=[('single_choice', 'Single choice'), ('multiple_choice', 'Multiple choice')], default='single_choice', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('task_type', models.CharField(choices=[('neutral', 'Neutral'), ('defense', 'Defense'), ('attack', 'Attack')], max_length=12)),
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=12)),
                ('acceptance_criteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.AcceptanceCriteria')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='catalog.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Virtualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('virtualization_role', models.CharField(choices=[('user_shell', 'User Shell'), ('user_accessible', 'User-accessible via IP')], max_length=30)),
                ('docker_compose_file', models.FileField(upload_to='')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='virtualizations', to='catalog.Task')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='catalog.Question')),
            ],
        ),
        migrations.CreateModel(
            name='HelpfulResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('url', models.URLField()),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helpful_resources', to='catalog.Classroom')),
            ],
        ),
        migrations.CreateModel(
            name='ClassroomInstructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classroominstructor_added_by', to=settings.AUTH_USER_MODEL)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Classroom')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroominstructor_instructor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='instructors',
            field=models.ManyToManyField(related_name='classrooms', through='catalog.ClassroomInstructor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='acceptancecriteria',
            name='questions',
            field=models.ManyToManyField(blank=True, to='catalog.Question'),
        ),
    ]
