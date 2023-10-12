from rest_framework import serializers

from authentication.models import User
from catalog.models import (Classroom, Project, ClassroomInstructor, HelpfulResource,
                            Task, Virtualization, AcceptanceCriteria, Question, QuestionChoice)

from drf_writable_nested.serializers import WritableNestedModelSerializer


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

    class Meta:
        model = AcceptanceCriteria
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.criteria_type = validated_data.get('criteria_type', instance.criteria_type)
        if instance.criteria_type == AcceptanceCriteria.MANUAL:
            instance.questions.clear()
            instance.regex = ""
            instance.flag = ""
        elif instance.criteria_type == AcceptanceCriteria.QUESTIONNAIRE:
            questions_data = validated_data.pop('questions', [])

            for question_data in questions_data:
                question_id = question_data.pop('id', None)

                if question_id:
                    question_instance = Question.objects.get(id=question_id)
                    question_serializer = QuestionSerializer(question_instance, data=question_data)
                else:
                    # Use the nested serializer to handle both Question and its Choices creation
                    question_serializer = QuestionSerializer(data=question_data)

                # This will handle both creation of new Questions and updating existing ones
                if question_serializer.is_valid():
                    question_serializer.save()
            instance.regex = ""
            instance.flag = ""
        elif instance.criteria_type == AcceptanceCriteria.REGEX:
            instance.questions.clear()
            instance.regex = validated_data.get('regex', instance.regex)
            instance.flag = ""
        elif instance.criteria_type == AcceptanceCriteria.FLAG:
            instance.questions.clear()
            instance.flag = validated_data.get('flag', instance.flag)
            instance.regex = ""

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.criteria_type == AcceptanceCriteria.MANUAL:
            data.pop('questions', None)
            data.pop('regex', None)
            data.pop('flag', None)
        elif instance.criteria_type == AcceptanceCriteria.QUESTIONNAIRE:
            data.pop('regex', None)
            data.pop('flag', None)
        elif instance.criteria_type == AcceptanceCriteria.REGEX:
            data.pop('questions', None)
            data.pop('flag', None)
        elif instance.criteria_type == AcceptanceCriteria.FLAG:
            data.pop('questions', None)
            data.pop('regex', None)

        return data

    def validate(self, data):
        criteria_type = data.get('criteria_type')

        if criteria_type == AcceptanceCriteria.MANUAL:
            if data.get('questions') or data.get('regex') or data.get('flag'):
                raise serializers.ValidationError("For MANUAL type, questions, regex, and flag should not be provided.")

        elif criteria_type == AcceptanceCriteria.QUESTIONNAIRE:
            if not data.get('questions') or data.get('regex') or data.get('flag'):
                raise serializers.ValidationError("For QUESTIONNAIRE type, only questions should be provided.")

        elif criteria_type == AcceptanceCriteria.REGEX:
            if data.get('questions') or not data.get('regex') or data.get('flag'):
                raise serializers.ValidationError("For REGEX type, only regex should be provided.")

        elif criteria_type == AcceptanceCriteria.FLAG:
            if data.get('questions') or data.get('regex') or not data.get('flag'):
                raise serializers.ValidationError("For FLAG type, only flag should be provided.")

        return data


class VirtualizationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    virtualization_role = serializers.CharField()
    docker_compose_file = serializers.FileField(read_only=True)

    class Meta:
        model = Virtualization
        fields = ['id', 'name', 'virtualization_role', 'docker_compose_file']


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


class UserSerializer(serializers.ModelSerializer):
    # The ID is the only field that is not read-only because it is used to identify a certain User
    id = serializers.IntegerField()
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ClassroomInstructorSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    instructor = UserSerializer()
    added_at = serializers.DateTimeField(read_only=True)
    # TODO: This should be read-only as well and automatically be filled with the current user
    added_by = UserSerializer()

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
        title = data.get('title')

        # Prevent duplicate classroom titles
        queryset = Classroom.objects.all()
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.filter(title=title).exists():
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
