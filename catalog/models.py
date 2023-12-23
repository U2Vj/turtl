from django.db import models
from rules import is_authenticated
from rules.contrib.models import RulesModel
from .predicates import manages_classroom, manages_project, manages_task
from authentication.models import User
from authentication.predicates import is_instructor
from django.utils.translation import gettext_lazy as _


class Regex(models.Model):
    """
    A regex is a regular expression that is used to check whether the user has completed the task.
    """
    prompt = models.CharField(max_length=200)
    pattern = models.CharField(max_length=200)


class Flag(models.Model):
    """
    A flag is a string that the user has to submit to prove that they have completed the task.
    """
    prompt = models.CharField(max_length=200)
    value = models.CharField(max_length=200)


class Question(models.Model):
    """
    A question that the user has to answer to prove that they have completed the task.
    Part of a quiz.
    """

    # The question that the user has to answer to prove that they have completed the task
    question = models.CharField(max_length=200)

    # The different types a question can have
    class QuestionType(models.TextChoices):
        SINGLE_CHOICE = 'SINGLE_CHOICE', _('Single choice')
        MULTIPLE_CHOICE = 'MULTIPLE_CHOICE', _('Multiple choice')

    # Type of the question, i.e. whether it is a single choice or multiple choice question
    question_type = models.CharField(choices=QuestionType.choices, default=QuestionType.SINGLE_CHOICE, max_length=15)


class QuestionChoice(models.Model):
    """
    A QuestionChoice is a possible answer to a question.
    """

    # A possible answer to the question
    answer = models.CharField(max_length=200)
    # Whether this answer is correct
    is_correct = models.BooleanField(default=False)
    # Linking each choice to a question
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')


class AcceptanceCriteria(models.Model):
    """
    An AcceptanceCriteria is a set of rules that define how the user can prove that they have completed the task.
    This is the superclass of all supported acceptance criteria types.
    """

    # The different types the AcceptanceCriteria of a task can have
    class CriteriaType(models.TextChoices):
        DISABLED = 'DISABLED', _('Disabled')
        MANUAL = 'MANUAL', _('Manual')
        QUIZ = 'QUIZ', _('Quiz')
        REGEX = 'REGEX', _('Regular expression')
        FLAG = 'FLAG', _('Flag')
        MIXED = 'MIXED', _('Mixed')

    criteria_type = models.CharField(choices=CriteriaType.choices, default=CriteriaType.DISABLED, max_length=8)

    # Additional fields for each criteria type, if necessary
    questions = models.ManyToManyField(Question, blank=True)
    regexes = models.ManyToManyField(Regex, blank=True)
    flags = models.ManyToManyField(Flag, blank=True)

    # Add any other common fields for all criteria types here

    def __str__(self):
        return f"{self.get_criteria_type_display()} Acceptance Criteria"


class Classroom(RulesModel):
    """
        A Classroom has a title, a description, a created_at timestamp and an updated_at timestamp.
        It has a ManyToMany relationship (instructors) to the User model and a OneToMany relationship to the
        Project model.
    """

    # A Classroom has a title e.g.: Eternal Blue Exploit
    title = models.CharField(max_length=120, unique=True)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # The Instructors who own this classroom
    instructors = models.ManyToManyField(User,
                                         through="ClassroomInstructor",
                                         through_fields=('classroom', 'instructor'),
                                         related_name='classrooms')

    # Permissions (Administrators automatically have all permissions)
    class Meta:
        rules_permissions = {
            # Authenticated Instructors can create classrooms in our application
            "add": is_authenticated & is_instructor,
            # Viewing classrooms is allowed for every authenticated instructor
            "view": is_authenticated & is_instructor,
            # To edit an existing classroom, you must be able to create one and also manage the one you are trying to
            # modify
            "change": is_authenticated & is_instructor & manages_classroom,
            # The same applies for deleting classrooms
            "delete": is_authenticated & is_instructor & manages_classroom
        }


class ClassroomInstructor(models.Model):
    """
        This model defines the relationship between a Classroom and a User (i.e. an instructor). It consists of
        the two necessary foreign keys and a timestamp added_at which saves when this instructor was added to the
        Classroom. It also contains an added_by field which references the user who added the instructor to the
        Classroom.
    """
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classroominstructor_instructor')
    added_at = models.DateTimeField(auto_now_add=True)

    # Please note that it is possible for a user to delete their account. When instructor A added another instructor B
    # but instructor A deletes their account, the relationship between instructor B and the Classroom still
    # exists. However, the user (instructor A) who added instructor B might not. In this case, the added_by field
    # should be set to NULL (which is why it is nullable).
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name='classroominstructor_added_by')

    class Meta:
        unique_together = ('classroom', 'instructor',)


class HelpfulResource(models.Model):
    title = models.CharField(max_length=120)

    url = models.URLField(max_length=200)

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="helpful_resources")


class Project(RulesModel):
    """
        A Project is contained within a classroom. It consists of a title and some tasks.
    """

    # Title of the Project
    title = models.CharField(max_length=120)

    # The corresponding classroom which this Project is a part of
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='projects')

    # Permissions (Administrators automatically have all permissions)
    class Meta:
        rules_permissions = {
            # Only instructors managing the specific classroom can add a project
            "add": is_authenticated & is_instructor,
            # All authenticated instructors can view projects
            "view": is_authenticated & is_instructor,
            # Only instructors who manage the classroom that the project belongs to can change it
            "change": is_authenticated & is_instructor & manages_project,
            # Only instructors managing the specific classroom can delete a project
            "delete": is_authenticated & is_instructor & manages_project,
        }
        unique_together = ('title', 'classroom',)


class Task(RulesModel):
    """
        A Task is part of a Project.
    """

    # Title of the Task
    title = models.CharField(max_length=50)

    # The project that this Task belongs to
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    # Description of the Task
    description = models.TextField()

    # Tasks can have one of three types: neutral, attack and defense
    class TaskType(models.TextChoices):
        NEUTRAL = 'NEUTRAL', _('Neutral')
        DEFENSE = 'DEFENSE', _('Defense')
        ATTACK = 'ATTACK', _('Attack')

    task_type = models.CharField(choices=TaskType.choices, default=TaskType.NEUTRAL, max_length=7)

    # Tasks have a difficulty level (beginner, intermediate or advanced)
    class Difficulty(models.TextChoices):
        BEGINNER = 'BEGINNER', _('Beginner')
        INTERMEDIATE = 'INTERMEDIATE', _('Intermediate')
        ADVANCED = 'ADVANCED', _('Advanced')

    difficulty = models.CharField(choices=Difficulty.choices, max_length=12)

    # The acceptance criteria for this Task, meaning how the user can prove that they have completed the task
    acceptance_criteria = models.ForeignKey(AcceptanceCriteria, on_delete=models.CASCADE)

    # Permissions (Administrators automatically have all permissions)
    class Meta:
        rules_permissions = {
            # Instructors can only add tasks if they manage the classroom associated with the project of the task
            "add": is_authenticated & is_instructor,
            # Tasks can be viewed by all authenticated instructors
            "view": is_authenticated & is_instructor,
            # Editing a task is restricted to instructors managing the related classroom
            "change": is_authenticated & is_instructor & manages_task,
            # Deleting a task follows the same permission requirements as editing
            "delete": is_authenticated & is_instructor & manages_task,
        }
        unique_together = ('title', 'project',)


class Virtualization(models.Model):
    """
        A Virtualization is a virtual machine that is created for a task.
    """

    # Name of the virtualization
    name = models.CharField(max_length=30)

    # The task that this virtualization belongs to
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='virtualizations')

    # Virtualizations have a role: they are either a shell visible to the user, or accessible by the user shell
    # via an IP address
    class Role(models.TextChoices):
        USER_SHELL = 'USER_SHELL', _('User Shell')
        USER_ACCESSIBLE = 'USER_ACCESSIBLE', _('User-accessible via IP')

    virtualization_role = models.CharField(choices=Role.choices, max_length=15)

    # File of the Dockerfile that is used to create the virtualization
    dockerfile = models.TextField()
