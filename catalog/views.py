from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from catalog.models import Classroom, Task, Project, ClassroomInstructor
from catalog.serializers import (ClassroomSerializer, ProjectDetailSerializer,
                                 TaskSerializer, ClassroomDetailSerializer,
                                 ProjectNewSerializer, TaskNewSerializer)
from turtl.utils.permissions import AutoPermissionViewSetWithListMixin


class ClassroomViewSet(AutoPermissionViewSetWithListMixin, ModelViewSet):
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()

    def perform_create(self, serializer):
        classroom: Classroom = serializer.save()
        ClassroomInstructor.objects.create(instructor=self.request.user,
                                           classroom=classroom,
                                           added_by=self.request.user).save()


class MyClassroomsViewSet(AutoPermissionViewSetWithListMixin, ModelViewSet):
    serializer_class = ClassroomSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.classrooms


class ClassroomDetailViewSet(AutoPermissionViewSetMixin, ModelViewSet):
    serializer_class = ClassroomDetailSerializer
    queryset = Classroom.objects.all()


class ProjectViewSet(AutoPermissionViewSetMixin, ModelViewSet):
    serializer_class = ProjectNewSerializer
    queryset = Project.objects.all()


class ProjectDetailViewSet(AutoPermissionViewSetMixin, ModelViewSet):
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()


class TaskViewSet(AutoPermissionViewSetMixin, ModelViewSet):
    serializer_class = TaskNewSerializer
    queryset = Task.objects.all()


class TaskDetailViewSet(AutoPermissionViewSetMixin, ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
