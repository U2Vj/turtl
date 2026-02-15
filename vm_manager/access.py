from catalog.predicates import manages_task
from enrollments.models import Enrollment


def user_can_access_task_vm(user, task) -> bool:
    if user.is_administrator:
        return True

    if user.is_instructor:
        return manages_task(user, task)

    if user.is_student:
        classroom = task.project.classroom
        return Enrollment.objects.filter(student=user, classroom=classroom).exists()

    return False
