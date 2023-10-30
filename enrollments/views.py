from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from catalog.models import Classroom
from turtl.utils.permissions import AutoPermissionViewSetWithListMixin
from .models import Enrollment
from .serializers import EnrollmentSerializer


class EnrollmentViewSet(AutoPermissionViewSetWithListMixin, ModelViewSet):
    permission_classes = (IsAuthenticated,)  # A user must be authenticated to access their enrollments
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        classroom_id = self.request.data.get('classroom')
        student = self.request.user

        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except ObjectDoesNotExist:
            raise ValidationError('The classroom you\'re trying to enroll in does not exist.')

        if Enrollment.objects.filter(classroom=classroom_id, student=student).exists():
            raise ValidationError('You are already enrolled in this classroom.')

        serializer.save(student=student)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Enrollment.DoesNotExist:
            raise NotFound("Enrollment not found.")

        if instance.student != self.request.user and not self.request.user.is_administrator:
            raise PermissionDenied('You do not have permission to delete this enrollment.')

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
