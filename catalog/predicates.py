import rules


@rules.predicate
def manages_classroom_template(user, classroom_template):
    return classroom_template.managers.filter(id=user.id).exists()
