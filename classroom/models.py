from django.db import models


# A Classroom is the connection between a user and an virtual environment.
# It keeps some description etc. of the vulnerability the virtual environment has.
class Classroom(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # One classroom has one virtual environment, which can be started from the classroom.
    environment = models.OneToOneField(
        'environment.VirtualEnvironment',
        on_delete=models.CASCADE
    )

    # One classroom can be owned by one user(Admin/Teacher)
    # After implementation of a Teacher role it can be changed to
    # authentication.Teacher
    owner = models.OneToOneField(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='classroom_owner'
    )

    # Many users can be members of many classrooms.
    member = models.ManyToManyField(
        'authentication.User',
        related_name='classroom_user'
    )

    # A classroom has a title e.g.: Eternal Blue Exploit
    title = models.CharField(max_length=30)

    # A classroom has a description e.g.: Eternal Blue is the exploit CVE-2017-0144
    description = models.TextField()

    # Define toString method
    def __str__(self):
        return self.title
