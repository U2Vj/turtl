from django.db import models
from rules import is_authenticated
from rules.contrib.models import RulesModel

from authentication.models import User
from authentication.predicates import is_instructor
from catalog.models import Classroom, Task
from enrollments.predicates import owns_enrollment, manages_enrollment_classroom


class Enrollment(RulesModel):
    """
    An enrollment is created when a student enrolls in a classroom.
    """
    id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    date_enrolled = models.DateTimeField(auto_now_add=True, editable=False)
    # TODO for later: last_visited = models.DateTimeField()

    def get_progress(self):
        number_of_tasks_total = 0
        for project in self.classroom.projects.all():
            number_of_tasks_total += project.tasks.all().count()

        if number_of_tasks_total == 0:
            return 100

        number_of_tasks_solved = self.solutions.all().count()

        return round((number_of_tasks_solved / number_of_tasks_total) * 100)

    class Meta:
        unique_together = ('classroom', 'student',)
        rules_permissions = {
            "add": is_authenticated,
            "view": is_authenticated & (owns_enrollment | (is_instructor & manages_enrollment_classroom)),
            "delete": is_authenticated & (owns_enrollment | (is_instructor & manages_enrollment_classroom)),
        }


class TaskSolution(RulesModel):
    """
    A TaskSolution is created when a student submits a solution to a task.
    """
    id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, editable=False, related_name='solutions')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, editable=False, related_name='solutions')
    date_submitted = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('enrollment', 'task',)
        rules_permissions = {
            "add": is_authenticated,
            "view": is_authenticated,
        }
