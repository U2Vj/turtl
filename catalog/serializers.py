from rest_framework import serializers

from authentication.models import User
from catalog.models import ClassroomTemplate, ProjectTemplate, ClassroomTemplateManager, HelpfulResource, TaskTemplate, \
    Virtualization, AcceptanceCriteria, Question


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question.QuestionChoice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, read_only=False)

    class Meta:
        model = Question
        fields = '__all__'


class AcceptanceCriteriaSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=False)

    class Meta:
        model = AcceptanceCriteria
        fields = '__all__'


class TaskTemplateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    virtualization = serializers.SerializerMethodField()
    acceptance_criteria = AcceptanceCriteriaSerializer()

    class Meta:
        model = TaskTemplate
        fields = ['id', 'title', 'virtualization', 'acceptance_criteria']

    def get_virtualization(self, task_template):
        virtualization = Virtualization.objects.filter(template=task_template.id)
        virtualization_serializer = VirtualizationSerializer(virtualization, many=True)
        return virtualization_serializer.data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)

        # Handle virtualization update
        virtualization_data = validated_data.pop('virtualization', [])
        for item_data in virtualization_data:
            virtualization_instance = Virtualization.objects.get(id=item_data['id'])
            virtualization_serializer = VirtualizationSerializer(virtualization_instance, data=item_data)
            if virtualization_serializer.is_valid():
                virtualization_serializer.save()

        # Handle acceptance criteria update
        acceptance_criteria_data = validated_data.pop('acceptance_criteria', None)
        if acceptance_criteria_data:
            acceptance_criteria_instance = instance.acceptance_criteria
            acceptance_criteria_serializer = AcceptanceCriteriaSerializer(acceptance_criteria_instance,
                                                                          data=acceptance_criteria_data)
            if acceptance_criteria_serializer.is_valid():
                acceptance_criteria_serializer.save()

        instance.save()
        return instance




class VirtualizationSerializer(serializers.Serializer):
    name = serializers.CharField()
    virtualization_role = serializers.CharField()
    docker_compose_file = serializers.FileField()

    class Meta:
        model = Virtualization
        fields = ['name', 'virtualization_role', 'docker_compose_file']


class ProjectTemplateDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    classroom_template_id = serializers.IntegerField()

    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title', 'classroom_template_id']


class ProjectTemplateClassroomSerializer(serializers.ModelSerializer):
    task_templates = TaskTemplateSerializer(many=True)

    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title', 'task_templates']

    def update(self, instance, validated_data):
        task_templates_data = validated_data.pop('task_templates', [])

        # Update the project template's fields
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Handle existing and new task templates
        for task_template_data in task_templates_data:
            task_template_id = task_template_data.get('id', None)
            if task_template_id:
                task_template = instance.task_templates.get(id=task_template_id)
                task_template_serializer = TaskTemplateSerializer(task_template, data=task_template_data, partial=True)
                if task_template_serializer.is_valid():
                    task_template_serializer.save()
            else:
                # Create new task template
                task_template_data['project_template'] = instance
                task_template_serializer = TaskTemplateSerializer(data=task_template_data)
                if task_template_serializer.is_valid():
                    task_template_serializer.save()

        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ClassroomTemplateManagerSerializer(serializers.Serializer):
    manager = serializers.SerializerMethodField()
    added_at = serializers.DateTimeField()

    class Meta:
        model = ClassroomTemplateManager
        fields = ['manager', 'added_at']

    def get_manager(self, obj):
        user = obj.manager
        user_serializer = UserSerializer(user)
        return user_serializer.data


class HelpfulResourceSerializer(serializers.Serializer):
    title = serializers.CharField()
    url = serializers.CharField()

    class Meta:
        model = HelpfulResource
        fields = ['title', 'url']


class ClassroomTemplateDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    project_templates = ProjectTemplateClassroomSerializer(many=True)
    helpful_resources = HelpfulResourceSerializer(many=True)
    managers = serializers.SerializerMethodField()

    def get_managers(self, classroom_template_id):
        classroom_template_managers = ClassroomTemplateManager.objects.filter(classroom_template=classroom_template_id)
        classroom_template_manager_serializer = ClassroomTemplateManagerSerializer(classroom_template_managers,
                                                                                   many=True)
        return classroom_template_manager_serializer.data

    def update(self, instance, validated_data):
        project_templates_data = validated_data.pop('project_templates', [])
        helpful_resources_data = validated_data.pop('helpful_resources', [])
        instance = super().update(instance, validated_data)

        # Handle existing project templates
        for project_template_data in project_templates_data:
            project_template_id = project_template_data.get('id', None)
            if project_template_id:
                project_template = instance.project_templates.get(id=project_template_id)
                project_template_serializer = ProjectTemplateClassroomSerializer(project_template,
                                                                                 data=project_template_data,
                                                                                 partial=True)
                if project_template_serializer.is_valid():
                    project_template_serializer.save()
            else:
                project_template_data['classroom_template'] = instance
                project_template_serializer = ProjectTemplateClassroomSerializer(data=project_template_data)
                if project_template_serializer.is_valid():
                    project_template_serializer.save()

        return instance

    class Meta:
        model = ClassroomTemplate
        fields = ['id', 'title', 'created_at', 'updated_at', 'project_templates', 'helpful_resources', 'managers']


class ClassroomTemplateSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = ClassroomTemplate
        fields = ['id', 'title', 'created_at', 'updated_at']


class ClassroomTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()

    def create(self, validated_data):
        return ClassroomTemplate.objects.create(**validated_data)


class ProjectTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()
    classroom_templates = serializers.CharField()

    def create(self, validated_data):
        project_template = ProjectTemplate.objects.create(title=validated_data.get('title'),
                                                          classroom_templates_id=validated_data.get(
                                                              'classroom_templates'))
        return project_template


class TaskTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    project_template_id = serializers.IntegerField()
