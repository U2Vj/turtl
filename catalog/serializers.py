from rest_framework import serializers

from authentication.models import User
from catalog.models import ClassroomTemplate, ProjectTemplate, ClassroomTemplateManager, HelpfulResource, TaskTemplate, \
    Virtualization, AcceptanceCriteria, Question, QuestionChoice

from drf_writable_nested.serializers import WritableNestedModelSerializer


class QuestionChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    answer = serializers.CharField()
    is_correct = serializers.BooleanField()

    class Meta:
        model = QuestionChoice
        fields = ['id', 'answer', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
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


class TaskTemplateSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    task_type = serializers.ChoiceField(choices=TaskTemplate.TASK_TYPE_CHOICES)
    difficulty = serializers.ChoiceField(choices=TaskTemplate.DIFFICULTY_CHOICES)
    virtualizations = VirtualizationSerializer(many=True)
    acceptance_criteria = AcceptanceCriteriaSerializer()

    class Meta:
        model = TaskTemplate
        fields = ['id', 'title', 'description', 'task_type', 'difficulty', 'virtualizations', 'acceptance_criteria']


class ProjectTemplateDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()

    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title']


class ProjectTemplateClassroomSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    task_templates = TaskTemplateSerializer(many=True)

    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title', 'task_templates']


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ClassroomTemplateManagerSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    added_at = serializers.DateTimeField()

    class Meta:
        model = ClassroomTemplateManager
        fields = ['id', 'user', 'added_at']


class HelpfulResourceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    url = serializers.CharField()

    class Meta:
        model = HelpfulResource
        fields = ['id', 'title', 'url']


class ClassroomTemplateDetailSerializer(WritableNestedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    project_templates = ProjectTemplateClassroomSerializer(many=True)
    helpful_resources = HelpfulResourceSerializer(many=True)
    managers = ClassroomTemplateManagerSerializer(many=True)

    class Meta:
        model = ClassroomTemplate
        fields = ['id', 'title', 'created_at', 'updated_at', 'project_templates', 'helpful_resources',
                  'managers']


class ClassroomTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomTemplate
        fields = ['id', 'title', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectTemplateNewSerializer(serializers.ModelSerializer):
    classroom_template_id = serializers.PrimaryKeyRelatedField(source='classroom_template',
                                                               queryset=ClassroomTemplate.objects.all())

    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title', 'classroom_template_id']
        read_only_fields = ['id']


class TaskTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    project_template_id = serializers.IntegerField()
