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

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        acceptance_criteria = AcceptanceCriteria.objects.create(**validated_data)
        for question_data in questions_data:
            choices_data = question_data.pop('choices')
            question = Question.objects.create(**question_data)
            acceptance_criteria.questions.add(question)
            for choice_data in choices_data:
                Question.QuestionChoice.objects.create(question=question, **choice_data)
        return acceptance_criteria

    def update(self, instance, validated_data):
        instance.criteria_type = validated_data.get('criteria_type', instance.criteria_type)
        if instance.criteria_type == AcceptanceCriteria.MANUAL:
            instance.questions.clear()
            instance.regex = ""
            instance.flag = ""
        elif instance.criteria_type == AcceptanceCriteria.QUESTIONNAIRE:
            questions_data = validated_data.pop('questions', None)
            new_questions = []
            if questions_data:
                for question_data in questions_data:
                    question_id = question_data.pop('id', None)
                    if question_id:
                        question = Question.objects.get(id=question_id)
                        for key, value in question_data.items():
                            setattr(question, key, value)
                        question.save()
                    else:
                        question = Question.objects.create(**question_data)
                    new_questions.append(question)
            instance.questions.set(new_questions)  # Use set() here
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


class TaskTemplateSerializer(serializers.Serializer):
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
    helpful_resources = serializers.SerializerMethodField()
    managers = serializers.SerializerMethodField()

    def get_project_templates(self, classroom_template):
        project_templates = ProjectTemplate.objects.filter(classroom_template=classroom_template)
        return ProjectTemplateClassroomSerializer(project_templates, many=True).data

    def get_managers(self, classroom_template_id):
        classroom_template_managers = ClassroomTemplateManager.objects.filter(classroom_template=classroom_template_id)
        classroom_template_manager_serializer = ClassroomTemplateManagerSerializer(classroom_template_managers,
                                                                                   many=True)
        return classroom_template_manager_serializer.data

    def get_helpful_resources(self, classroom_template_id):
        helpful_resources = HelpfulResource.objects.filter(classroom_template_id=classroom_template_id)
        helpful_resource_serializer = HelpfulResourceSerializer(helpful_resources, many=True)
        return helpful_resource_serializer.data

    def update(self, instance, validated_data):
        project_templates_data = validated_data.pop('project_templates', [])
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
