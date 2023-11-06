import rules


@rules.predicate
def manages_classroom(user, classroom):
    return classroom.instructors.filter(id=user.id).exists()


@rules.predicate
def manages_project(user, project):
    return project.classroom.instructors.filter(id=user.id).exists()


@rules.predicate
def manages_task(user, task):
    return task.project.classroom.instructors.filter(id=user.id).exists()
