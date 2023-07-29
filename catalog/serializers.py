from rest_framework import serializers

from authentication.models import User
from catalog.models import ClassroomTemplate, ProjectTemplate, ClassroomTemplateManager, HelpfulResource, TaskTemplate, \
    Virtualization, AcceptanceCriteria, AcceptanceCriteriaFlag, AcceptanceCriteriaRegex, AcceptanceCriteriaQuestionnaire


class AcceptanceCriteriaSerializer(serializers.Serializer):
    class Meta:
        model = AcceptanceCriteria


class AcceptanceCriteriaFlagSerializer(AcceptanceCriteriaSerializer):
    type = serializers.CharField()
    flag = serializers.CharField()

    class Meta:
        model = AcceptanceCriteriaFlag
        fields = ['type', 'flag']



class AcceptanceCriteriaRegexSerializer(serializers.Serializer):
    type = serializers.CharField()
    regex = serializers.CharField()

    class Meta:
        model = AcceptanceCriteriaRegex
        fields = ['type', 'regex']


class AcceptanceCriteriaQuestionnaireSerializer(serializers.Serializer):
    type = serializers.CharField()
    questions = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = AcceptanceCriteriaQuestionnaire
        fields = ['type', 'questions']


class TaskTemplateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    virtualization = serializers.SerializerMethodField()
    acceptance_criteria = serializers.SerializerMethodField()

    class Meta:
        model = TaskTemplate
        fields = ['id', 'title', 'virtualization', 'acceptance_criteria', 'type', 'regex', 'flag', 'questions']

    def get_virtualization(self, task_template):
        virtualization = Virtualization.objects.filter(template=task_template.id)
        virtualization_serializer = VirtualizationSerializer(virtualization, many=True)
        return virtualization_serializer.data

    def get_acceptance_criteria(self, task_template):
        acceptance_criteria = task_template.objects.filter(task_template_id=task_template.id)
        acceptance_criteria_serializer = AcceptanceCriteriaSerializer(acceptance_criteria, many=True)
        return acceptance_criteria_serializer.data

    def get_acceptance_criteria(self, obj):
        if isinstance(obj.acceptance_criteria, AcceptanceCriteriaFlag):
            serializer = AcceptanceCriteriaFlagSerializer(obj.acceptance_criteria)
        elif isinstance(obj.acceptance_criteria, AcceptanceCriteriaRegex):
            serializer = AcceptanceCriteriaRegexSerializer(obj.acceptance_criteria)
        elif isinstance(obj.acceptance_criteria, AcceptanceCriteriaQuestionnaire):
            serializer = AcceptanceCriteriaQuestionnaireSerializer(obj.acceptance_criteria)


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




class ProjectTemplateClassroomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    task_templates = TaskTemplateSerializer(many=True)

    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title', 'task_templates']

    def get_task_templates(self, project_template):
        task_templates = ProjectTemplate.objects.filter(project_template=project_template)
        return TaskTemplateSerializer(task_templates, many=True).data

    def update(self, instance, validated_data):
        task_templates_data = validated_data.pop('task_templates', [])
        instance = super().update(instance, validated_data)

        for task_template_data in task_templates_data:
            task_template_id = task_template_data.get('id', None)
            if task_template_id:
                try:
                    task_template = instance.task_templates.get(id=task_template_id)
                    for attr, value in task_template_data.items():
                        setattr(task_template, attr, value)
                    task_template.save()
                except TaskTemplate.DoesNotExist:
                    pass

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

    def get_User(self, manager_id):
        user = User.objects.get(id=manager_id)
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
    helpful_resources = serializers.SerializerMethodField()
    managers = serializers.SerializerMethodField()

    def get_project_templates(self, classroom_template):
        project_templates = ProjectTemplate.objects.filter(classroom_template=classroom_template)
        return ProjectTemplateClassroomSerializer(project_templates, many=True).data

    def get_managers(self, classroom_template_id):
        classroom_template_managers = ClassroomTemplateManager.objects.filter(classroom_template=classroom_template_id)
        classroom_template_manager_serializer = ClassroomTemplateManagerSerializer(classroom_template_managers, many=True)
        return classroom_template_manager_serializer.data

    def get_helpful_resources(self, classroom_template_id):
        helpful_resources = HelpfulResource.objects.filter(classroom_template_id=classroom_template_id)
        helpful_resource_serializer = HelpfulResourceSerializer(helpful_resources, many=True)
        return helpful_resource_serializer.data


    def update(self, instance, validated_data):
        project_templates_data = validated_data.pop('project_templates', [])
        instance = super().update(instance, validated_data)

        for project_template_data in project_templates_data:
            project_template_id = project_template_data.get('id', None)
            if project_template_id:
                try:
                    project_template = instance.project_templates.get(id=project_template_id)
                    for attr, value in project_template_data.items():
                        if attr == 'task_templates':
                            task_templates = project_template.task_templates.all()
                            for task in task_templates:
                                task.delete()
                            for task_data in value:
                                TaskTemplate.objects.create(project_template=project_template, **task_data)
                        else:
                            setattr(project_template, attr, value)
                    project_template.save()
                except ProjectTemplate.DoesNotExist:
                    pass

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
        project_template = ProjectTemplate.objects.create(title=validated_data.get('title'), classroom_templates_id=validated_data.get('classroom_templates'))
        return project_template



class TaskTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    project_template_id = serializers.IntegerField()
