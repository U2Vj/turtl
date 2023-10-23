from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from authentication.models import User
from authentication.serializers import UserSerializer
from catalog.models import (Classroom, Project, ClassroomInstructor, HelpfulResource,
                            Task, Virtualization, AcceptanceCriteria, Question, QuestionChoice,
                            Regex, Flag)

from drf_writable_nested.serializers import WritableNestedModelSerializer


class RegexSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    pattern = serializers.CharField()

    class Meta:
        model = Regex
        fields = '__all__'


class FlagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    prompt = serializers.CharField(allow_blank=True)
    value = serializers.CharField()

    class Meta:
        model = Flag
        fields = '__all__'


class QuestionChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    answer = serializers.CharField()
    is_correct = serializers.BooleanField()

    class Meta:
        model = QuestionChoice
        fields = ['id', 'answer', 'is_correct']


class QuestionSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    choices = QuestionChoiceSerializer(required=False, many=True, read_only=False)
    question = serializers.CharField()
    question_type = serializers.ChoiceField(choices=Question.QUESTION_TYPE_CHOICES, default=Question.SINGLE_CHOICE)

    class Meta:
        model = Question
        fields = '__all__'


class AcceptanceCriteriaSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    questions = QuestionSerializer(many=True, read_only=False, required=False)
    regexes = RegexSerializer(many=True, read_only=False, required=False)
    flags = FlagSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = AcceptanceCriteria
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.criteria_type = validated_data.get('criteria_type', instance.criteria_type)

        instance = super().update(instance, validated_data)

        if instance.criteria_type == AcceptanceCriteria.MANUAL or instance.criteria_type == AcceptanceCriteria.DISABLED:
            instance.questions.clear()
            instance.regexes.clear()
            instance.flags.clear()
        elif instance.criteria_type == AcceptanceCriteria.QUESTIONNAIRE:
            instance.regexes.clear()
            instance.flags.clear()
        elif instance.criteria_type == AcceptanceCriteria.REGEX:
            instance.questions.clear()
            instance.flags.clear()
        elif instance.criteria_type == AcceptanceCriteria.FLAG:
            instance.questions.clear()
            instance.regexes.clear()

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.criteria_type == AcceptanceCriteria.MANUAL or instance.criteria_type == AcceptanceCriteria.DISABLED:
            data.pop('questions', None)
            data.pop('regexes', None)
            data.pop('flags', None)
        elif instance.criteria_type == AcceptanceCriteria.QUESTIONNAIRE:
            data.pop('regexes', None)
            data.pop('flags', None)
        elif instance.criteria_type == AcceptanceCriteria.REGEX:
            data.pop('questions', None)
            data.pop('flags', None)
        elif instance.criteria_type == AcceptanceCriteria.FLAG:
            data.pop('questions', None)
            data.pop('regexes', None)

        return data

    def validate(self, data):
        criteria_type = data.get('criteria_type')

        if criteria_type == AcceptanceCriteria.MANUAL:
            if data.get('questions') or data.get('regexes') or data.get('flags'):
                raise serializers.ValidationError("For MANUAL type, questions, regex, and flag should not be provided.")

        elif criteria_type == AcceptanceCriteria.DISABLED:
            if data.get('questions') or data.get('regexes') or data.get('flags'):
                raise serializers.ValidationError("For DISABLED type, questions, regex, and flag should not be "
                                                  "provided.")

        elif criteria_type == AcceptanceCriteria.QUESTIONNAIRE:
            if not data.get('questions') or data.get('regexes') or data.get('flags'):
                raise serializers.ValidationError("For QUESTIONNAIRE type, only questions should be provided.")

        elif criteria_type == AcceptanceCriteria.REGEX:
            if data.get('questions') or not data.get('regexes') or data.get('flags'):
                raise serializers.ValidationError("For REGEX type, only regex should be provided.")

        elif criteria_type == AcceptanceCriteria.FLAG:
            if data.get('questions') or data.get('regexes') or not data.get('flags'):
                raise serializers.ValidationError("For FLAG type, only flag should be provided.")

        return data


class VirtualizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Virtualization
        fields = ['id', 'name', 'virtualization_role', 'dockerfile']
        read_only_fields = ['id']


class TaskNewSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    project_id = serializers.IntegerField()


class TaskSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    task_type = serializers.ChoiceField(choices=Task.TASK_TYPE_CHOICES)
    difficulty = serializers.ChoiceField(choices=Task.DIFFICULTY_CHOICES)
    virtualizations = VirtualizationSerializer(many=True)
    acceptance_criteria = AcceptanceCriteriaSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'task_type', 'difficulty', 'virtualizations', 'acceptance_criteria']


class ProjectNewSerializer(serializers.ModelSerializer):
    classroom_id = serializers.PrimaryKeyRelatedField(source='classroom',
                                                      queryset=Classroom.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'title', 'classroom_id']
        read_only_fields = ['id']


class ProjectDetailSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'tasks']


class ClassroomInstructorSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    instructor = UserSerializer()
    added_at = serializers.DateTimeField(read_only=True)
    added_by = UserSerializer(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        instructor_data = validated_data.pop('instructor')

        try:
            instructor = User.objects.get(id=instructor_data['id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Instructor does not exist.")

        if instructor.role != User.Role.INSTRUCTOR:
            raise serializers.ValidationError("User is not an instructor.")

        instance = ClassroomInstructor.objects.create(added_by=user, instructor=instructor, **validated_data)
        return instance

    class Meta:
        model = ClassroomInstructor
        fields = ['id', 'instructor', 'added_at', 'added_by']


class HelpfulResourceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=120)
    url = serializers.URLField(max_length=200)

    class Meta:
        model = HelpfulResource
        fields = ['id', 'title', 'url']


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'title', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClassroomDetailSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
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

        return data

    class Meta:
        model = Classroom
        fields = ['id', 'title', 'created_at', 'updated_at', 'projects', 'helpful_resources',
                  'instructors']
