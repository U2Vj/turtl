from django.db import models


# A virtueal enviornment can host a vulnerable application etc.
# to showcase an exploit.
class VirtualEnvironment(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)


# A DockerEnvironment is a virtual environment using the docker demon and
# containers to isolate the vulnerable application.
class DockerEnvironment(VirtualEnvironment):
    # The yaml file with the description of the docker containers etc.
    yaml = models.FileField()
