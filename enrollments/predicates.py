import rules
from catalog.predicates import manages_classroom


@rules.predicate
def owns_enrollment(user, enrollment):
    return enrollment.student.id == user.id


@rules.predicate
def manages_enrollment_classroom(user, enrollment):
    return manages_classroom(user, enrollment.classroom)
