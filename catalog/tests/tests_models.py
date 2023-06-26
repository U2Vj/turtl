from django.test import TestCase

from authentication.models import User
from catalog.models import ClassroomTemplate, ClassroomTemplateManager


class ClassroomTemplateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # we'll create 3 users: one instructor, one manager and one administrator

        User.objects.create_instructor("John Doe", "john@doe.com", "12345678")
        User.objects.create_manager("Jack Doe", "jack@doe.com", "12345678")
        User.objects.create_administrator("Sarah Doe", "sarah@doe.com", "12345678")

    def test_permissions_create(self):

        # get our newly created test users
        instructor = User.objects.get(id=1)
        manager = User.objects.get(id=2)
        administrator = User.objects.get(id=3)

        # managers and administrators can create classroom templates
        self.assertTrue(manager.has_perm("catalog.add_classroomtemplate"))
        self.assertTrue(administrator.has_perm("catalog.add_classroomtemplate"))

        self.assertFalse(instructor.has_perm("catalog.add_classroomtemplate"))

    def set_up_classroom_template(self):

        instructor = User.objects.get(id=1)
        manager = User.objects.get(id=2)
        administrator = User.objects.get(id=3)

        # let's create a new classroom template
        classroom_template = ClassroomTemplate.objects.create(title="Test Classroom Template", description="abc def")
        classroom_template.save()

        classroom_template_manager1 = ClassroomTemplateManager.objects.create(manager=manager,
                                                                              classroom_template=classroom_template,
                                                                              added_by=manager)
        classroom_template_manager1.save()

        return instructor, manager, administrator, classroom_template, classroom_template_manager1

    def test_permissions_edit(self):

        instructor, manager, administrator, classroom_template, classroom_template_manager1 = \
            self.set_up_classroom_template()

        # Managers can edit their own classrooms
        self.assertTrue(manager.has_perm("catalog.change_classroomtemplate", classroom_template))

        # Instructors cannot
        self.assertFalse(instructor.has_perm("catalog.change_classroomtemplate", classroom_template))

        # Administrators always can
        self.assertTrue(administrator.has_perm("catalog.change_classroomtemplate", classroom_template))

    def test_permissions_delete(self):

        instructor, manager, administrator, classroom_template, classroom_template_manager1 = \
            self.set_up_classroom_template()

        # Managers can delete their own classrooms
        self.assertTrue(manager.has_perm("catalog.delete_classroomtemplate", classroom_template))

        # Instructors cannot
        self.assertFalse(instructor.has_perm("catalog.delete_classroomtemplate",  classroom_template))

        # Administrators can do anything
        self.assertTrue(administrator.has_perm("catalog.delete_classroomtemplate", classroom_template))






