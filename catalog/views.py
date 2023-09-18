from django.http import Http404

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from catalog.models import Classroom, Task, Project, ClassroomInstructor
from catalog.serializers import (ClassroomSerializer, ProjectClassroomSerializer,
                                 TaskSerializer, ClassroomDetailSerializer,
                                 ProjectNewSerializer, ClassroomInstructorSerializer)


class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    # TODO: Add permission classes once they're working again


class ClassroomDetailViewSet(ModelViewSet):
    serializer_class = ClassroomDetailSerializer

    def get_queryset(self):
        classroom_id: int = self.kwargs['pk']
        return Classroom.objects.filter(id=classroom_id)


class ClassroomDetail(APIView):
    def get_object(self, classroom_id):
        try:
            return Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise Http404("Classroom not found")

    def get(self, request, classroom_id):
        classroom = self.get_object(classroom_id)
        serializer = ClassroomDetailSerializer(classroom)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, classroom_id):
        classroom = self.get_object(classroom_id)
        serializer = ClassroomDetailSerializer(classroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def delete(self, request, classroom_id):
        classroom = self.get_object(classroom_id)
        classroom.delete()
        return Response(status=status.HTTP_200_OK)


class ProjectNew(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectNewSerializer


class ProjectDetail(APIView):
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            serializer = ProjectClassroomSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            serializer = ProjectClassroomSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return Response(status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class TaskNew(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ClassroomInstructorViewSet(ModelViewSet):
    queryset = ClassroomInstructor.objects.all()
    serializer_class = ClassroomInstructorSerializer
