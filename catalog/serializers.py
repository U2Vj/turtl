from rest_framework import serializers
from catalog.models import ClassroomTemplate


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
    task_templates = serializers.ListField()


class ClassroomTemplateSerializer(serializers.ModelSerializer):
    project_templates = serializers.ListField(child=serializers.IntegerField())
    information = serializers.DictField(child=serializers.CharField())
    helpful_resources = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))
    managers = ManagerSerializer(many=True)

    class Meta:
        model = ClassroomTemplate
        fields = ['id', 'project_templates', 'information', 'helpful_resources', 'managers']


class ClassroomTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()


class ProjectTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()
    classroom_template_id = serializers.IntegerField()


class TaskTemplateNewSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    project_template_id = serializers.IntegerField()
