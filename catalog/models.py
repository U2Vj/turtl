from django.db import models
from rules.contrib.models import RulesModel
from .predicates import manages_classroom_template
from authentication.models import User
from authentication.predicates import is_manager, is_administrator, is_instructor


class Question(models.Model):
    """
        A question that the user has to answer to prove that they have completed the task.
        Part of an AcceptanceCriteriaQuestionnaire.
    """

    # The question that the user has to answer to prove that they have completed the task
    question = models.CharField(max_length=200)

    class QuestionChoice(models.Model):
        """
            A QuestionChoice is a possible answer to a question.
        """

        # A possible answer to the question
        answer = models.CharField(max_length=200)
        # Whether this answer is correct
        is_correct = models.BooleanField(default=False)

    # The possible choices for the question
    choices = models.ManyToManyField(QuestionChoice, related_name='questionChoices')

    SINGLE_CHOICE = 0  # Single choice question
    MULTIPLE_CHOICE = 1  # Multiple choice question

    # Possible choices for the question type
    QUESTION_TYPE_CHOICES = [
        (SINGLE_CHOICE, "Single choice"),
        (MULTIPLE_CHOICE, "Multiple choice")
    ]

    # Type of the question, i.e. whether it is a single choice or multiple choice question
    question_type = models.IntegerField(choices=QUESTION_TYPE_CHOICES, default=SINGLE_CHOICE)


class AcceptanceCriteria(models.Model):
    """
    An AcceptanceCriteria is a set of rules that define how the user can prove that they have completed the task.
    This is the superclass of all supported acceptance criteria types.
    """

    MANUAL = 'manual'
    QUESTIONNAIRE = 'questionnaire'
    REGEX = 'regex'
    FLAG = 'flag'

    CRITERIA_TYPE_CHOICES = [
        (MANUAL, 'Manual'),
        (QUESTIONNAIRE, 'Questionnaire'),
        (REGEX, 'Regex'),
        (FLAG, 'Flag'),
    ]

    criteria_type = models.CharField(
        choices=CRITERIA_TYPE_CHOICES,
        default=MANUAL,
        max_length=20
    )

    # Additional fields for each criteria type, if necessary
    questions = models.ManyToManyField(Question, blank=True)
    regex = models.CharField(max_length=200, blank=True)
    flag = models.CharField(max_length=50, blank=True)

    # Add any other common fields for all criteria types here

    def __str__(self):
        return f"{self.get_criteria_type_display()} Acceptance Criteria"


class ClassroomTemplate(RulesModel):
    """
        A ClassroomTemplate has a title, a description, a created_at timestamp and an updated_at timestamp.
        It has a ManyToMany relationship (managers) to the User model and a ManyToMany relationship to the
        ProjectTemplate model.
    """

    # A ClassroomTemplate has a title e.g.: Eternal Blue Exploit
    title = models.CharField(max_length=120, unique=True)

    # A ClassroomTemplate has a description e.g.: Eternal Blue is the exploit CVE-2017-0144
    description = models.TextField()

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    managers = models.ManyToManyField(User, related_name='classroom_templates', through="ClassroomTemplateManager",
                                      through_fields=('classroom_template', 'manager'))

    # Permissions
    class Meta:
        rules_permissions = {
            # Managers and administrators can create classroom templates in our application
            "add": is_manager | is_administrator,
            # Reading classroom templates is allowed for instructors, managers and administrators
            "read": is_instructor | is_manager | is_administrator,
            # To edit an existing classroom template, you must be able to create one and also manage the one you are
            # trying to modify
            "change": (is_manager | is_administrator) & manages_classroom_template,
            # Additionally, administrators can always delete classroom templates
            "delete": (is_manager & manages_classroom_template) | is_administrator
        }


class ClassroomTemplateManager(models.Model):
    """
        This model defines the relationship between a ClassroomTemplate and a User (i.e. a manager). It consists of the
        two necessary foreign keys and a timestamp added_at which saves when this manager was added to the
        ClassroomTemplate. It also contains an added_by field which references the user who added the manager to the
        ClassroomTemplate.
    """
    classroom_template = models.ForeignKey(ClassroomTemplate, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classroomtemplatemanager_set_manager')
    added_at = models.DateTimeField(auto_now_add=True)

    # Please note that it is possible for a user to delete their account. When manager A added another manager B but
    # manager A deletes their account, the relationship between manager B and the ClassroomTemplate still exists.
    # However, the user (manager A) who added manager B might not. In this case, the added_by field should be set to
    # NULL (which is why it is nullable).
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name='classroomtemplatemanager_set_added_by')


class HelpfulResource(models.Model):
    title = models.CharField(max_length=120, unique=True)

    url = models.URLField(max_length=200)

    classroom_template = models.ForeignKey(ClassroomTemplate, on_delete=models.CASCADE,
                                           related_name="helpful_resources")


class ProjectTemplate(RulesModel):
    """
        A ProjectTemplate is a template that is used to create a Project.
    """

    # Title of the project
    title = models.CharField(max_length=120)

    classroom_templates = models.ForeignKey(ClassroomTemplate, on_delete=models.CASCADE,
                                            related_name='project_templates')


class TaskTemplate(models.Model):
    """
        A TaskTemplate is a template that is used to create a Task.
    """

    # Title of the task
    title = models.CharField(max_length=50)

    # The project template that this task template belongs to
    project_template = models.ForeignKey(ProjectTemplate, on_delete=models.CASCADE, related_name='task_templates')

    # Description of the task
    description = models.TextField()

    NEUTRAL = 'N'  # Neutral type
    DEFENSE = 'DE'  # Defense type
    ATTACK = 'AT'  # Attack type

    # Possible choices for the task type
    TASK_TYPE_CHOICES = [
        (NEUTRAL, "Neutral"),
        (DEFENSE, "Defense"),
        (ATTACK, "Attack")
    ]

    # Type of the task, i.e. whether it is a neutral, defense or attack task
    task_type = models.CharField(choices=TASK_TYPE_CHOICES, max_length=12)

    BEGINNER = "Beginner"  # Beginner difficulty
    INTERMEDIATE = "Intermediate"  # Intermediate difficulty
    ADVANCED = "Advanced"  # Advanced difficulty

    # Possible choices for the difficulty of a task
    DIFFICULTY_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced")
    ]

    # Difficulty of the task
    difficulty = models.CharField(choices=DIFFICULTY_CHOICES, max_length=12)

    # The acceptance criteria for this task, meaning how the user can prove that they have completed the task
    acceptance_criteria = models.ForeignKey(AcceptanceCriteria, on_delete=models.CASCADE)


class Virtualization(models.Model):
    """
        A Virtualization is a virtual machine that is created for a task.
    """

    # Name of the virtualization
    name = models.CharField(max_length=30)

    # The task template that this virtualization belongs to
    template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='virtualizations')

    USER_SHELL = "User Shell"  # The user interacts with the virtualization via a shell
    USER_ACCESSIBLE = "User-accessible via IP"  # The user interacts with the virtualization via an IP address

    # Choices for the virtualization role (i.e. how the user interacts with the virtualization)
    ROLE_CHOICES = [
        (USER_SHELL, "User Shell"),
        (USER_ACCESSIBLE, "User-accessible via IP"),
    ]

    # Role of virtualization (i.e. how the user interacts with the virtualization)
    virtualization_role = models.CharField(choices=ROLE_CHOICES, max_length=30)

    # File of the docker-compose.yml that is used to create the virtualization
    docker_compose_file = models.FileField(upload_to='')