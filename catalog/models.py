from django.db import models

from authentication.models import User


class ProjectTemplate(models.Model):
    pass


class ClassroomTemplate(models.Model):
    """
        A ClassroomTemplate has a title, a description, a created_at timestamp and an updated_at timestamp.
        It has a ManyToMany relationship (managers) to the User model and a ManyToMany relationship to the
        ProjectTemplate model.
    """
    # A ClassroomTemplate has a title e.g.: Eternal Blue Exploit
    title = models.CharField(max_length=120)

    # A ClassroomTemplate has a description e.g.: Eternal Blue is the exploit CVE-2017-0144
    description = models.TextField()

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    managers = models.ManyToManyField(User, related_name='classroom_templates', through="ClassroomTemplateManager",
                                      through_fields=('classroom_template', 'manager'))

    project_templates = models.ManyToManyField(ProjectTemplate, related_name='classroom_templates')


class ClassroomTemplateManager(models.Model):
    """
        This model defines the relationship between a ClassroomTemplate and a User (i.e. a manager). It consists of the
        two necessary foreign keys and a timestamp added_at which saves when this manager was added to the
        ClassroomTemplate. It also contains an added_by field which references the user who added the manager to the
        ClassroomTemplate.
    """
    classroom_template = models.ForeignKey(ClassroomTemplate, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classroomtemplatemanager_set_manager')
    added_at = models.DateTimeField(auto_now_add=True)

    # Please note that it is possible for a user to delete their account. When manager A added another manager B but
    # manager A deletes their account, the relationship between manager B and the ClassroomTemplate still exists.
    # However, the user (manager A) who added manager B might not. In this case, the added_by field should be set to
    # NULL (which is why it is nullable).
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name='classroomtemplatemanager_set_added_by')
