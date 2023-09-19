import rules


@rules.predicate
def manages_classroom(user, classroom):
    print(user)
    print(classroom)
    return classroom.instructors.filter(id=user.id).exists()
