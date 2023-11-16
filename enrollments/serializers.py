from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.serializers import UserSerializer
from catalog.models import Classroom
from catalog.serializers import ClassroomSerializer, ClassroomDetailSerializer
from .models import Enrollment, TaskSolution


class EnrollmentSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
        error_messages={'does_not_exist': 'The classroom you are trying to enroll in does not exist.'}
    )
    student = UserSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'classroom', 'student', 'date_enrolled']
        read_only_fields = ['id', 'student', 'date_enrolled']

    def validate_classroom(self, classroom):
        if Enrollment.objects.filter(classroom=classroom, student=self.context['request'].user).exists():
            raise ValidationError('You are already enrolled in this classroom.')
        return classroom

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['classroom'] = ClassroomSerializer(instance.classroom).data
        return rep


class ClassroomStudentSerializer(ClassroomDetailSerializer):
    instructors = UserSerializer(many=True)

    def to_representation(self, instance):
        classroom = super().to_representation(instance)

        # This is a serializer for students, hence we have to remove the
        # virtualizations and the solutions from the tasks

        for project in classroom['projects']:
            for task in project['tasks']:
                del task['virtualizations']

                if 'flags' in task['acceptance_criteria']:
                    for flag in task['acceptance_criteria']['flags']:
                        del flag['value']

                if 'regexes' in task['acceptance_criteria']:
                    for regex in task['acceptance_criteria']['regexes']:
                        del regex['pattern']

                if 'questions' in task['acceptance_criteria']:
                    for question in task['acceptance_criteria']['questions']:
                        for choice in question['choices']:
                            del choice['is_correct']

        return classroom


class EnrollmentDetailSerializer(serializers.ModelSerializer):
    classroom = ClassroomStudentSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        task_solutions = TaskSolution.objects.filter(enrollment=instance).select_related('task')
        solutions_dict = {solution.task_id: solution.date_submitted for solution in task_solutions}

        for project in representation['classroom']['projects']:
            for task in project['tasks']:
                task_id = task['id']
                task['done'] = task_id in solutions_dict
                task['date_submitted'] = solutions_dict.get(task_id)

        return representation

    class Meta:
        model = Enrollment
        fields = ['id', 'classroom', 'student', 'date_enrolled']
        read_only_fields = ['id', 'classroom', 'student', 'date_enrolled']


class EnrollmentUserSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'date_enrolled']
        read_only_fields = ['id', 'student', 'date_enrolled']


class TaskSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSolution
        fields = ['id', 'enrollment', 'task']
        read_only_fields = ['id', 'enrollment', 'task']


class RegexSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    solution = serializers.CharField()


class FlagSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    solution = serializers.CharField()


class QuestionSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    selected_choices = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
