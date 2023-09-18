import rules


@rules.predicate
def manages_classroom(user, classroom):
    return classroom.instructors.filter(id=user.id).exists()
