from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from catalog.models import Classroom
from catalog.predicates import manages_classroom
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentDetailSerializer, EnrollmentUserSerializer


class EnrollmentViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)  # A user must be authenticated to access their enrollments
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class EnrollmentDetailViewSet(AutoPermissionViewSetMixin, ModelViewSet):
    serializer_class = EnrollmentDetailSerializer
    queryset = Enrollment.objects.all()


class ClassroomEnrollmentListView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EnrollmentUserSerializer

    @action(detail=False, methods=['get'], url_path='for-classroom')
    def list_enrollments(self, request, pk=None):
        classroom = get_object_or_404(Classroom, pk=pk)

        if not request.user.is_administrator:
            if not request.user.is_instructor:
                return Response({"detail": "Access denied: User is not an instructor."},
                                status=status.HTTP_403_FORBIDDEN)
            if not manages_classroom(request.user, classroom):
                return Response({"detail": "Access denied: User does not manage this classroom."},
                                status=status.HTTP_403_FORBIDDEN)
        queryset = Enrollment.objects.filter(classroom=classroom)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
