from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from catalog.models import ClassroomTemplate, TaskTemplate, ProjectTemplate
from catalog.serializers import (ClassroomTemplateSerializer, ProjectTemplateClassroomSerializer,
                                 TaskTemplateSerializer, ClassroomTemplateDetailSerializer,
                                 ProjectTemplateNewSerializer)


class ClassroomTemplateViewSet(ModelViewSet):
    queryset = ClassroomTemplate.objects.all()
    serializer_class = ClassroomTemplateSerializer
    # TODO: Add permission classes once they're working again


class ClassroomTemplateDetail(APIView):
    def get_object(self, template_id):
        try:
            return ClassroomTemplate.objects.get(id=template_id)
        except ClassroomTemplate.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, template_id):
        template = self.get_object(template_id)
        serializer = ClassroomTemplateDetailSerializer(template)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, template_id):
        template = self.get_object(template_id)
        serializer = ClassroomTemplateDetailSerializer(template, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def delete(self, request, template_id):
        template = self.get_object(template_id)
        template.delete()
        return Response(status=status.HTTP_200_OK)

class ProjectTemplateList(APIView):
    def post(self, request):
        serializer = ProjectTemplateNewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectTemplateDetail(APIView):
    def get(self, request, project_id):
        try:
            template = ProjectTemplate.objects.get(id=project_id)
            serializer = ProjectTemplateClassroomSerializer(template)
            return Response(serializer.data)
        except ProjectTemplate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id):
        try:
            template = ProjectTemplate.objects.get(id=project_id)
            serializer = ProjectTemplateClassroomSerializer(template, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ProjectTemplate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, project_id):
        try:
            template = ProjectTemplate.objects.get(id=project_id)
            template.delete()
            return Response(status=status.HTTP_200_OK)
        except ProjectTemplate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TaskTemplateList(APIView):
    def post(self, request):
        serializer = TaskTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskTemplateDetail(APIView):
    def get(self, request, task_id):
        try:
            template = TaskTemplate.objects.get(id=task_id)
            serializer = TaskTemplateSerializer(template)
            return Response(serializer.data)
        except TaskTemplate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, task_id):
        try:
            template = TaskTemplate.objects.get(id=task_id)
            serializer = TaskTemplateSerializer(template, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TaskTemplate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

