from django.test import TestCase

from authentication.models import User
from catalog.models import Classroom, ClassroomInstructor


class ClassroomTemplateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # we'll create 3 users: one student, one instructor and one administrator
        User.objects.create_student("jack@doe.com", "12345678")
        User.objects.create_instructor("john@doe.com", "12345678")
        User.objects.create_administrator("sarah@doe.com", "12345678")

        # we'll create another instructor which does not have any classrooms
        User.objects.create_instructor("max@doe.com", "12345678")

    def test_permissions_create(self):

        # get our newly created test users
        student = User.objects.get(id=1)
        instructor = User.objects.get(id=2)
        administrator = User.objects.get(id=3)

        # instructors and administrators can create classroom templates
        self.assertTrue(instructor.has_perm("catalog.add_classroom"))
        self.assertTrue(administrator.has_perm("catalog.add_classroom"))

        # students cannot
        self.assertFalse(student.has_perm("catalog.add_classroom"))

    def set_up_classroom(self):

        student = User.objects.get(id=1)
        instructor = User.objects.get(id=2)
        administrator = User.objects.get(id=3)
        instructor2 = User.objects.get(id=4)

        # let's create a new classroom
        classroom = Classroom.objects.create(title="Test Classroom Template")
        classroom.save()

        classroom_instructor1 = ClassroomInstructor.objects.create(instructor=instructor,
                                                                   classroom=classroom,
                                                                   added_by=instructor)
        classroom_instructor1.save()

        return student, instructor, instructor2, administrator, classroom, classroom_instructor1

    def test_permissions_edit(self):

        student, instructor, instructor2, administrator, classroom, classroom_instructor1 = self.set_up_classroom()

        # Instructors can edit their own classrooms
        self.assertTrue(instructor.has_perm("catalog.change_classroom", classroom))
        self.assertFalse(instructor2.has_perm("catalog.change_classroom", classroom))

        # Students cannot
        self.assertFalse(student.has_perm("catalog.change_classroom", classroom))

        # Administrators always can
        self.assertTrue(administrator.has_perm("catalog.change_classroom", classroom))

    def test_permissions_delete(self):

        student, instructor, instructor2, administrator, classroom, classroom_instructor1 = self.set_up_classroom()

        # Instructors can delete their own classrooms
        self.assertTrue(instructor.has_perm("catalog.delete_classroom", classroom))
        self.assertFalse(instructor2.has_perm("catalog.delete_classroom", classroom))

        # Students cannot
        self.assertFalse(student.has_perm("catalog.delete_classroom",  classroom))

        # Administrators can do anything
        self.assertTrue(administrator.has_perm("catalog.delete_classroom", classroom))






