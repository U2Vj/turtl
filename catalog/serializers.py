import io
import re

from django.core.exceptions import ObjectDoesNotExist
from dockerfile_parse import DockerfileParser
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from authentication.models import User
from authentication.serializers import UserSerializer
from catalog.models import (Classroom, Project, ClassroomInstructor, HelpfulResource,
                            Task, Virtualization, AcceptanceCriteria, Question, QuestionChoice,
                            Regex, Flag)
from catalog.predicates import manages_classroom, manages_project


class RegexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Regex
        fields = '__all__'
        read_only_fields = ['id']

    @staticmethod
    def validate_pattern(value):
        try:
            re.compile(value)
        except re.error:
            raise serializers.ValidationError(f"The provided regex pattern '{value}' is invalid.")
        return value


class FlagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flag
        fields = '__all__'
        read_only_fields = ['id']


class QuestionChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionChoice
        fields = ['id', 'answer', 'is_correct']
        read_only_fields = ['id']


class QuestionSerializer(WritableNestedModelSerializer):
    choices = QuestionChoiceSerializer(required=False, many=True, read_only=False)
    question_type = serializers.ChoiceField(
        choices=Question.QuestionType.choices,
        default=Question.QuestionType.SINGLE_CHOICE
    )

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        choices = data.get('choices', [])
        if not choices:
            raise serializers.ValidationError("Each question must have at least one choice.")

        correct_answer_count = sum(choice.get('is_correct', False) for choice in choices)
        if data.get('question_type') == Question.QuestionType.SINGLE_CHOICE:
            if correct_answer_count != 1:
                raise serializers.ValidationError(
                    "A single choice question must have exactly one correct answer."
                )
        elif data.get('question_type') == Question.QuestionType.MULTIPLE_CHOICE:
            if correct_answer_count < 1:
                raise serializers.ValidationError(
                    "A multiple choice question must have at least one correct answer."
                )

        return super().validate(data)


class AcceptanceCriteriaSerializer(WritableNestedModelSerializer):
    questions = QuestionSerializer(many=True, read_only=False, required=False)
    regexes = RegexSerializer(many=True, read_only=False, required=False)
    flags = FlagSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = AcceptanceCriteria
        fields = '__all__'
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        instance.criteria_type = validated_data.get('criteria_type', instance.criteria_type)

        instance = super().update(instance, validated_data)

        if (instance.criteria_type == AcceptanceCriteria.CriteriaType.MANUAL
                or instance.criteria_type == AcceptanceCriteria.CriteriaType.DISABLED):
            instance.questions.clear()
            instance.regexes.clear()
            instance.flags.clear()
        elif instance.criteria_type == AcceptanceCriteria.CriteriaType.QUIZ:
            instance.regexes.clear()
            instance.flags.clear()
        elif instance.criteria_type == AcceptanceCriteria.CriteriaType.REGEX:
            instance.questions.clear()
            instance.flags.clear()
        elif instance.criteria_type == AcceptanceCriteria.CriteriaType.FLAG:
            instance.questions.clear()
            instance.regexes.clear()

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if (instance.criteria_type == AcceptanceCriteria.CriteriaType.MANUAL
                or instance.criteria_type == AcceptanceCriteria.CriteriaType.DISABLED):
            data.pop('questions', None)
            data.pop('regexes', None)
            data.pop('flags', None)
        elif instance.criteria_type == AcceptanceCriteria.CriteriaType.QUIZ:
            data.pop('regexes', None)
            data.pop('flags', None)
        elif instance.criteria_type == AcceptanceCriteria.CriteriaType.REGEX:
            data.pop('questions', None)
            data.pop('flags', None)
        elif instance.criteria_type == AcceptanceCriteria.CriteriaType.FLAG:
            data.pop('questions', None)
            data.pop('regexes', None)

        return data

    def validate(self, data):
        criteria_type = data.get('criteria_type')

        if criteria_type == AcceptanceCriteria.CriteriaType.MANUAL:
            if data.get('questions') or data.get('regexes') or data.get('flags'):
                raise serializers.ValidationError("For MANUAL type, "
                                                  "questions, regexes, and flags should not be provided.")

        elif criteria_type == AcceptanceCriteria.CriteriaType.DISABLED:
            if data.get('questions') or data.get('regexes') or data.get('flags'):
                raise serializers.ValidationError("For DISABLED type, "
                                                  "questions, regexes, and flags should not be provided.")

        elif criteria_type == AcceptanceCriteria.CriteriaType.QUIZ:
            if not data.get('questions') or data.get('regexes') or data.get('flags'):
                raise serializers.ValidationError("For QUIZ type, only questions should be provided.")

        elif criteria_type == AcceptanceCriteria.CriteriaType.REGEX:
            if data.get('questions') or not data.get('regexes') or data.get('flags'):
                raise serializers.ValidationError("For REGEX type, only regexes should be provided.")

        elif criteria_type == AcceptanceCriteria.CriteriaType.FLAG:
            if data.get('questions') or data.get('regexes') or not data.get('flags'):
                raise serializers.ValidationError("For FLAG type, only flags should be provided.")

        return super().validate(data)


class VirtualizationSerializer(serializers.ModelSerializer):
    virtualization_role = serializers.ChoiceField(choices=Virtualization.Role.choices)
    dockerfile = serializers.CharField()

    class Meta:
        model = Virtualization
        fields = ['id', 'name', 'virtualization_role', 'dockerfile']
        read_only_fields = ['id']

    @staticmethod
    def validate_dockerfile(value):
        dfp = DockerfileParser(fileobj=io.StringIO(value))

        if not dfp.baseimage:
            raise serializers.ValidationError("The Dockerfile must start with a FROM instruction.")

        instructions = dfp.structure
        if not any(instr['instruction'] == 'RUN' for instr in instructions):
            raise serializers.ValidationError("The Dockerfile should contain at least one RUN instruction.")

        return value


class TaskNewSerializer(WritableNestedModelSerializer):
    task_type = serializers.ChoiceField(choices=Task.TaskType.choices)
    difficulty = serializers.ChoiceField(choices=Task.Difficulty.choices)
    acceptance_criteria = AcceptanceCriteriaSerializer()
    project_id = serializers.PrimaryKeyRelatedField(source='project',
                                                    queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'task_type', 'difficulty', 'acceptance_criteria', 'project_id']
        read_only_fields = ['id']

    def validate(self, data):
        user = self.context['request'].user
        project = data.get('project')
        if not manages_project(user, project):
            raise serializers.ValidationError("You are not an instructor of this project.")
        return data


class TaskSerializer(WritableNestedModelSerializer):
    task_type = serializers.ChoiceField(choices=Task.TaskType.choices)
    difficulty = serializers.ChoiceField(choices=Task.Difficulty.choices)
    virtualizations = VirtualizationSerializer(many=True)
    acceptance_criteria = AcceptanceCriteriaSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'task_type', 'difficulty', 'virtualizations', 'acceptance_criteria']
        read_only_fields = ['id']


class ProjectNewSerializer(serializers.ModelSerializer):
    classroom_id = serializers.PrimaryKeyRelatedField(source='classroom',
                                                      queryset=Classroom.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'title', 'classroom_id']
        read_only_fields = ['id']

    def validate(self, data):
        user = self.context['request'].user
        classroom = data.get('classroom')
        if not manages_classroom(user, classroom):
            raise serializers.ValidationError("You are not an instructor of this classroom.")
        return data


class ProjectDetailSerializer(WritableNestedModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'tasks']
        read_only_fields = ['id']


class ClassroomInstructorSerializer(WritableNestedModelSerializer):
    instructor = UserSerializer()
    added_by = UserSerializer(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        instructor_data = validated_data.pop('instructor')

        try:
            instructor = User.objects.get(id=instructor_data['id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Instructor does not exist.")

        if not instructor.is_instructor and not instructor.is_administrator:
            raise serializers.ValidationError("User is not an instructor or administrator.")

        instance = ClassroomInstructor.objects.create(added_by=user, instructor=instructor, **validated_data)
        return instance

    class Meta:
        model = ClassroomInstructor
        fields = ['id', 'instructor', 'added_at', 'added_by']
        read_only_fields = ['id', 'added_at', 'added_by']


class HelpfulResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = HelpfulResource
        fields = ['id', 'title', 'url']
        read_only_fields = ['id']


class ClassroomSerializer(serializers.ModelSerializer):
    instructors = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'title', 'created_at', 'updated_at', 'instructors']
        read_only_fields = ['id', 'created_at', 'updated_at', 'instructors']


class ClassroomDetailSerializer(WritableNestedModelSerializer):
    projects = ProjectDetailSerializer(many=True)
    helpful_resources = HelpfulResourceSerializer(many=True)
    instructors = ClassroomInstructorSerializer(many=True, source='classroominstructor_set')

    def validate(self, data):
        # Prevent duplicate classroom titles
        queryset = Classroom.objects.all()
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.filter(title=data.get('title')).exists():
            raise serializers.ValidationError('This classroom title already exists.')

        # Prevent classrooms without instructors
        instructors = data.get('classroominstructor_set', [])
        if self.instance and not instructors:
            raise serializers.ValidationError('At least one instructor must be associated with the classroom.')

        # Prevent classrooms with duplicate instructors
        instructor_ids = [instructor['instructor']['id'] for instructor in instructors]
        if len(instructor_ids) != len(set(instructor_ids)):
            raise serializers.ValidationError('You cannot add duplicate instructors to a classroom.')

        return data

    class Meta:
        model = Classroom
        fields = ['id', 'title', 'created_at', 'updated_at', 'projects', 'helpful_resources',
                  'instructors']
        read_only_fields = ['id', 'created_at', 'updated_at']
