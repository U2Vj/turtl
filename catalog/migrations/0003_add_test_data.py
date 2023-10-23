# Generated by Django 3.0.7 on 2023-10-02 03:48

from django.db import migrations


def add_test_data(apps, schema_editor):
    # Fetch models
    User = apps.get_model('authentication', 'User')
    Classroom = apps.get_model('catalog', 'Classroom')
    ClassroomInstructor = apps.get_model('catalog', 'ClassroomInstructor')
    Project = apps.get_model('catalog', 'Project')
    Task = apps.get_model('catalog', 'Task')
    AcceptanceCriteria = apps.get_model('catalog', 'AcceptanceCriteria')
    Regex = apps.get_model('catalog', 'Regex')
    Flag = apps.get_model('catalog', 'Flag')
    Question = apps.get_model('catalog', 'Question')
    QuestionChoice = apps.get_model('catalog', 'QuestionChoice')
    Virtualization = apps.get_model('catalog', 'Virtualization')
    HelpfulResource = apps.get_model('catalog', 'HelpfulResource')

    # Fetch users
    student1 = User.objects.get(email='student@localhost')
    student2 = User.objects.get(email='student2@localhost')
    student3 = User.objects.get(email='student3@localhost')
    student4 = User.objects.get(email='student4@localhost')
    student5 = User.objects.get(email='student5@localhost')
    instructor1 = User.objects.get(email='instructor@localhost')
    instructor2 = User.objects.get(email='instructor2@localhost')
    instructor3 = User.objects.get(email='instructor3@localhost')
    admin = User.objects.get(email='admin@localhost')

    # Create test classrooms
    itsicherheit = Classroom.objects.create(title='IT-Sicherheit')
    rechnernetze = Classroom.objects.create(title='Rechnernetze')

    # Add instructors to classrooms
    ClassroomInstructor.objects.create(classroom=itsicherheit, instructor=instructor1, added_by=instructor1)
    ClassroomInstructor.objects.create(classroom=itsicherheit, instructor=instructor2, added_by=instructor1)
    ClassroomInstructor.objects.create(classroom=rechnernetze, instructor=instructor2, added_by=instructor2)
    ClassroomInstructor.objects.create(classroom=rechnernetze, instructor=instructor3, added_by=instructor2)

    # Create test projects
    sqlinjection = Project.objects.create(title='SQL Injection', classroom=itsicherheit)
    xss = Project.objects.create(title='Cross-Site Scripting', classroom=itsicherheit)
    bufferoverflow = Project.objects.create(title='Buffer Overflow', classroom=itsicherheit)
    ddos = Project.objects.create(title='DDoS', classroom=itsicherheit)
    tcpip = Project.objects.create(title='TCP/IP', classroom=rechnernetze)
    dns = Project.objects.create(title='DNS', classroom=rechnernetze)
    dhcp = Project.objects.create(title='DHCP', classroom=rechnernetze)

    # Create test questions
    sqlinjectionpythonq1 = Question.objects.create(question='Is this code safe from SQL Injection?', question_type='single_choice')
    xssq2 = Question.objects.create(question='Which of the following are types of XSS?', question_type='multiple_choice')

    # Create test question choices
    QuestionChoice.objects.create(answer='Yes', question=sqlinjectionpythonq1, is_correct=False)
    QuestionChoice.objects.create(answer='No', question=sqlinjectionpythonq1, is_correct=True)
    QuestionChoice.objects.create(answer='Reflected XSS', question=xssq2, is_correct=True)
    QuestionChoice.objects.create(answer='Stored XSS', question=xssq2, is_correct=True)
    QuestionChoice.objects.create(answer='DOM XSS', question=xssq2, is_correct=False)

    # Create test regexes and flags
    sqlinjectionjavaregex = Regex.objects.create(pattern='.*', prompt="Enter your solution")
    reflectedxssflag = Flag.objects.create(value='FL4G', prompt="Please enter the flag that you found")

    # Add acceptance criteria to tasks
    sqlinjectionpythonac = AcceptanceCriteria.objects.create(criteria_type='questionnaire')
    sqlinjectionjavaac = AcceptanceCriteria.objects.create(criteria_type='regex')
    reflectedxssac = AcceptanceCriteria.objects.create(criteria_type='flag')
    storedxssac = AcceptanceCriteria.objects.create(criteria_type='questionnaire')
    bufferoverflowcac = AcceptanceCriteria.objects.create(criteria_type='manual')

    sqlinjectionjavaac.regexes.add(sqlinjectionjavaregex)
    reflectedxssac.flags.add(reflectedxssflag)
    sqlinjectionpythonac.questions.set([sqlinjectionpythonq1])
    storedxssac.questions.set([xssq2])

    # Add tasks to projects
    sqlinjectionpython = Task.objects.create(title='SQL Injection in Python', description='SQL Injection in Python', task_type='attack', difficulty='beginner', project=sqlinjection, acceptance_criteria=sqlinjectionpythonac)
    sqlinjectionjava = Task.objects.create(title='SQL Injection in Java', description='SQL Injection in Java', task_type='attack', difficulty='beginner', project=sqlinjection, acceptance_criteria=sqlinjectionjavaac)
    reflectedxss = Task.objects.create(title='Reflected XSS', description='Reflected XSS', task_type='neutral', difficulty='intermediate', project=xss, acceptance_criteria=reflectedxssac)
    storedxss = Task.objects.create(title='Stored XSS', description='Stored XSS', task_type='neutral', difficulty='intermediate', project=xss, acceptance_criteria=storedxssac)
    bufferoverflowc = Task.objects.create(title='Buffer Overflow in C', description='Buffer Overflow in C', task_type='defense', difficulty='advanced', project=bufferoverflow, acceptance_criteria=bufferoverflowcac)

    # Add helpful resources to classrooms
    HelpfulResource.objects.create(title='SQL Injection', url='https://www.w3schools.com/sql/sql_injection.asp', classroom=itsicherheit)
    HelpfulResource.objects.create(title='XSS', url='https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting', classroom=itsicherheit)
    HelpfulResource.objects.create(title='Buffer Overflow', url='https://www.geeksforgeeks.org/buffer-overflow-attack-with-example/', classroom=itsicherheit)
    HelpfulResource.objects.create(title='DDoS', url='https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/', classroom=itsicherheit)


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0002_add_flag_regex_models'),
        ('authentication', '0009_add_test_users')
    ]

    operations = [
        migrations.RunPython(add_test_data),
    ]
