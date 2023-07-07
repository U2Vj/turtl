from rest_framework import serializers
from catalog.models import ClassroomTemplate, ProjectTemplate, ClassroomTemplateManager, HelpfulResource


class ManagerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.CharField()


class TaskTemplateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    virtualization = serializers.DictField()
    acceptance_criteria = serializers.ListField()


class AcceptanceCriteriaFlagSerializer(serializers.Serializer):
    type = serializers.CharField()
    flag = serializers.CharField()


class AcceptanceCriteriaRegexSerializer(serializers.Serializer):
    type = serializers.CharField()
    regex = serializers.CharField()


class AcceptanceCriteriaQuestionnaireSerializer(serializers.Serializer):
    type = serializers.CharField()
    questions = serializers.ListField(child=serializers.DictField())


class ProjectTemplateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title']


class ClassroomTemplateManagerSerializer:
    manager = UserSerializer()
    added_at = serializers.DateTimeField()


class HelpfulResourceSerializer:
    title = serializers.CharField()
    url = serializers.CharField()

    class Meta:
        model = HelpfulResource
        fields = ['title', 'url']


class ClassroomTemplateDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    project_templates = serializers.SerializerMethodField()
    helpful_resources = serializers.SerializerMethodField()
    managers = serializers.SerializerMethodField()

    def get_project_templates(self, classroom_template_id):
        project_templates = ProjectTemplate.objects.filter(classroom_templates_id=classroom_template_id)
        project_template_serializer = ProjectTemplateSerializer(project_templates, many=True)
        return project_template_serializer.data

    def get_classroom_template_managers(self, classroom_template_id):
        classroom_template_managers = ClassroomTemplateManager.objects.filter(classroom_template=classroom_template_id)
        classroom_template_manager_serializer = ClassroomTemplateManagerSerializer(classroom_template_managers, many=True)

    def get_helpful_resources(self, classroom_template_id):
        helpful_resources = HelpfulResource.objects.filter(classroom_templates_id=classroom_template_id)
        helpful_resource_serializer = HelpfulResourceSerializer(helpful_resources, many=True)
        return helpful_resource_serializer.data

    class Meta:
        model = ClassroomTemplate
        fields = ['id', 'title', 'created_at', 'updated_at', 'project_templates']
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
    classroom_template_id = serializers.IntegerField()

    def create(self, validated_data):
          return ProjectTemplate.objects.create(**validated_data)



class TaskTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    project_template_id = serializers.IntegerField()
