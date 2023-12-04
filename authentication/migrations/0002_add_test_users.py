from django.db import migrations
from django.contrib.auth.hashers import make_password


def add_test_users(apps, schema_editor):
    # Fetch user model
    User = apps.get_model('authentication', 'User')

    # Hashed passwords
    hashed_student_password = make_password('student')
    hashed_instructor_password = make_password('instructor')
    hashed_admin_password = make_password('admin')

    # Create test students
    User.objects.create(email='student@localhost', password=hashed_student_password, role='STUDENT')
    User.objects.create(email='student2@localhost', password=hashed_student_password, role='STUDENT')
    User.objects.create(email='student3@localhost', password=hashed_student_password, role='STUDENT')
    User.objects.create(email='student4@localhost', password=hashed_student_password, role='STUDENT')
    User.objects.create(email='student5@localhost', password=hashed_student_password, role='STUDENT')

    # Create test instructors
    User.objects.create(
        email='instructor@localhost',
        username='Prof. Dr. Test Instructor',
        password=hashed_instructor_password,
        role='INSTRUCTOR'
    )
    User.objects.create(email='instructor2@localhost', password=hashed_instructor_password, role='INSTRUCTOR')
    User.objects.create(email='instructor3@localhost', password=hashed_instructor_password, role='INSTRUCTOR')

    # Create test administrator
    User.objects.create(email='admin@localhost', password=hashed_admin_password, role='ADMINISTRATOR')


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_test_users),
    ]