from rest_framework import serializers

from catalog.models import Classroom
from catalog.serializers import ClassroomSerializer
from .models import Enrollment, TaskSolution


class EnrollmentSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())

    class Meta:
        model = Enrollment
        fields = ['id', 'classroom', 'student', 'date_enrolled']
        read_only_fields = ['id', 'student', 'date_enrolled']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['classroom'] = ClassroomSerializer(instance.classroom).data
        return rep


class TaskSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSolution
        fields = ['id', 'enrollment', 'task']
        read_only_fields = ['id', 'enrollment', 'task']
