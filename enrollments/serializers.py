from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from authentication.serializers import UserSerializer
from catalog.models import Classroom, Project, Task
from catalog.serializers import ClassroomSerializer, ClassroomDetailSerializer, ProjectDetailSerializer, TaskSerializer
from .models import Enrollment, TaskSolution


class EnrollmentUserSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    progress = SerializerMethodField()

    @staticmethod
    def get_progress(enrollment):
        return enrollment.get_progress()

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'date_enrolled', 'progress']
        read_only_fields = ['id', 'student', 'date_enrolled', 'progress']


class EnrollmentSerializer(EnrollmentUserSerializer):
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
        error_messages={'does_not_exist': 'The classroom you are trying to enroll in does not exist.'}
    )

    class Meta:
        model = Enrollment
        fields = ['id', 'classroom', 'student', 'date_enrolled', 'progress']
        read_only_fields = ['id', 'student', 'date_enrolled', 'progress']

    def validate_classroom(self, classroom):
        if Enrollment.objects.filter(classroom=classroom, student=self.context['request'].user).exists():
            raise ValidationError('You are already enrolled in this classroom.')
        return classroom

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['classroom'] = ClassroomSerializer(instance.classroom).data
        return rep


class TaskStudentSerializer(TaskSerializer):
    done = SerializerMethodField()
    date_submitted = SerializerMethodField()

    def get_done(self, task):
        enrollment: Enrollment = self.context['enrollment']
        return enrollment.solutions.filter(task=task).exists()

    def get_date_submitted(self, task):
        enrollment: Enrollment = self.context['enrollment']
        solution = enrollment.solutions.filter(task=task).first()
        if solution is None:
            return None
        return solution.date_submitted

    def to_representation(self, instance):
        # This is a serializer for students, hence we have to remove every acceptance criteria solution from the task

        representation = super().to_representation(instance)

        if 'flags' in representation['acceptance_criteria']:
            for flag in representation['acceptance_criteria']['flags']:
                del flag['value']

        if 'regexes' in representation['acceptance_criteria']:
            for regex in representation['acceptance_criteria']['regexes']:
                del regex['pattern']

        if 'questions' in representation['acceptance_criteria']:
            for question in representation['acceptance_criteria']['questions']:
                for choice in question['choices']:
                    del choice['is_correct']

        return representation

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'task_type', 'difficulty', 'acceptance_criteria', 'done',
                  'date_submitted']


class ProjectStudentSerializer(ProjectDetailSerializer):
    tasks = SerializerMethodField()
    progress = SerializerMethodField()

    def get_tasks(self, project):
        return TaskStudentSerializer(
            many=True,
            instance=project.tasks,
            read_only=True,
            context=self.context
        ).data

    def get_progress(self, project: Project):
        enrollment: Enrollment = self.context['enrollment']
        number_of_total_tasks = project.tasks.all().count()
        if number_of_total_tasks == 0:
            return 100
        number_of_solved_tasks = enrollment.solutions.filter(task__in=project.tasks.all()).count()
        return round((number_of_solved_tasks / number_of_total_tasks) * 100)

    class Meta:
        model = Project
        fields = ['id', 'title', 'tasks', 'progress']


class ClassroomStudentDetailSerializer(ClassroomDetailSerializer):
    instructors = UserSerializer(many=True)
    projects = SerializerMethodField()

    def get_projects(self, classroom):
        return ProjectStudentSerializer(
            many=True,
            instance=classroom.projects,
            read_only=True,
            context=self.context
        ).data


class EnrollmentDetailSerializer(EnrollmentUserSerializer):
    classroom = SerializerMethodField(read_only=True)

    @staticmethod
    def get_classroom(enrollment):
        return ClassroomStudentDetailSerializer(
            instance=enrollment.classroom,
            context={'enrollment': enrollment},
            read_only=True
        ).data

    class Meta:
        model = Enrollment
        fields = ['id', 'classroom', 'student', 'date_enrolled', 'progress']
        read_only_fields = ['id', 'classroom', 'student', 'date_enrolled', 'progress']


class TaskSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSolution
        fields = ['id', 'enrollment', 'task', 'date_submitted']
        read_only_fields = ['id', 'enrollment', 'task', 'date_submitted']


class RegexSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    solution = serializers.CharField()


class FlagSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    solution = serializers.CharField()


class QuestionSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    selected_choices = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)


class TaskSubmissionSerializer(serializers.Serializer):
    regexes = RegexSubmissionSerializer(many=True)
    flags = FlagSubmissionSerializer(many=True)
    questions = QuestionSubmissionSerializer(many=True)
