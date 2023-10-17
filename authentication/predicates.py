import rules


@rules.predicate
def is_administrator(user):
    return user.is_administrator


@rules.predicate
def is_instructor(user):
    return user.is_instructor


@rules.predicate
def is_student(user):
    return user.is_student


@rules.predicate
def issued_invitation(user, invitation):
    return invitation.issuer == user
