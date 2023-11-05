import rules


@rules.predicate
def manages_classroom(user, classroom):
    print(user)
    print(classroom)  # TODO: Remove this
    return classroom.instructors.filter(id=user.id).exists()
