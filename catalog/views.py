from django.http import Http404

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from catalog.models import Classroom, Task, Project, ClassroomInstructor
from catalog.serializers import (ClassroomSerializer, ProjectDetailSerializer,
                                 TaskSerializer, ClassroomDetailSerializer,
                                 ProjectNewSerializer, ClassroomInstructorSerializer)
from turtl.utils.permissions import AutoPermissionViewSetWithListMixin


class ClassroomViewSet(AutoPermissionViewSetWithListMixin, ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def perform_create(self, serializer):
        classroom: Classroom = serializer.save()
        ClassroomInstructor.objects.create(instructor=self.request.user,
                                           classroom=classroom,
                                           added_by=self.request.user).save()


class ClassroomDetailViewSet(AutoPermissionViewSetMixin, ModelViewSet):
    serializer_class = ClassroomDetailSerializer
    queryset = Classroom.objects.all()


class ProjectNew(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectNewSerializer


class ProjectDetailViewSet(ModelViewSet):
    serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        project_id: int = self.kwargs['pk']
        return Project.objects.filter(id=project_id)


class TaskNew(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        task_id: int = self.kwargs['pk']
        return Task.objects.filter(id=task_id)


class ClassroomInstructorViewSet(ModelViewSet):
    queryset = ClassroomInstructor.objects.all()
    serializer_class = ClassroomInstructorSerializer
