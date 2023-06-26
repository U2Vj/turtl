import rules


@rules.predicate
def is_administrator(user):
    return user.is_administrator


@rules.predicate
def is_manager(user):
    return user.is_manager


@rules.predicate
def is_instructor(user):
    return user.is_instructor


@rules.predicate
def is_student(user):
    return user.is_student
