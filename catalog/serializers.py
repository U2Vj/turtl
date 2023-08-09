from rest_framework import serializers

from authentication.models import User
from catalog.models import ClassroomTemplate, ProjectTemplate, ClassroomTemplateManager, HelpfulResource, TaskTemplate, \
    Virtualization, AcceptanceCriteria, Question, QuestionChoice


class QuestionChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    answer = serializers.CharField()
    is_correct = serializers.BooleanField()

    class Meta:
        model = QuestionChoice
        fields = ['id', 'answer', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    choices = QuestionChoiceSerializer(required=False, many=True, read_only=False)
    question = serializers.CharField()
    question_type = serializers.ChoiceField(choices=Question.QUESTION_TYPE_CHOICES, default=Question.SINGLE_CHOICE)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        # Extract choices data from the validated_data
        choices_data = validated_data.pop('choices', [])

        # Create the Question instance
        question = Question.objects.create(**validated_data)

        # Create related QuestionChoice instances
        for choice_data in choices_data:
            if 'id' in choice_data:
                choice_data.pop('id')
            QuestionChoice.objects.create(question=question, **choice_data)

        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # Handle choices
        if choices_data:
            new_choices = []
            for choice_data in choices_data:
                choice_id = choice_data.pop('id', None)
                if choice_id:
                    choice_instance = QuestionChoice.objects.get(id=choice_id)
                    for k, v in choice_data.items():
                        setattr(choice_instance, k, v)
                    choice_instance.save()
                else:
                    choice_instance = QuestionChoice.objects.create(question=instance, **choice_data)
                    new_choices.append(choice_instance)

            # Update the question's choices
            instance.choices.set(new_choices)

        return instance


class AcceptanceCriteriaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    questions = QuestionSerializer(many=True, read_only=False, required=False)

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
                QuestionChoice.objects.create(question=question, **choice_data)
        return acceptance_criteria

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


class TaskTemplateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    title = serializers.CharField()
    description = serializers.CharField()
    task_type = serializers.ChoiceField(choices=TaskTemplate.TASK_TYPE_CHOICES)
    difficulty = serializers.ChoiceField(choices=TaskTemplate.DIFFICULTY_CHOICES)
    virtualizations = VirtualizationSerializer(many=True)
    acceptance_criteria = AcceptanceCriteriaSerializer()

    class Meta:
        model = TaskTemplate
        fields = ['id', 'title', 'description', 'task_type', 'difficulty', 'virtualizations', 'acceptance_criteria']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.task_type = validated_data.get('task_type', instance.task_type)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)

        # Handle virtualization update
        virtualizations_data = validated_data.pop('virtualizations', [])
        for virtualization_data in virtualizations_data:
            virtualization_id = virtualization_data.get('id')
            virtualization_instance = Virtualization.objects.get(id=virtualization_id)
            virtualization_serializer = VirtualizationSerializer(virtualization_instance, data=virtualization_data,
                                                                 partial=True)

            if virtualization_serializer.is_valid():
                virtualization_serializer.save(template=instance)

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


class ProjectTemplateDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = ProjectTemplate
        fields = ['id', 'title']


class ProjectTemplateClassroomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
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
            task_template = instance.task_templates.get(id=task_template_id)
            task_template_serializer = TaskTemplateSerializer(task_template, data=task_template_data, partial=True)
            if task_template_serializer.is_valid():
                task_template_serializer.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ClassroomTemplateManagerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    added_at = serializers.DateTimeField()

    class Meta:
        model = ClassroomTemplateManager
        fields = ['id', 'user', 'added_at']


class HelpfulResourceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    url = serializers.CharField()

    class Meta:
        model = HelpfulResource
        fields = ['id', 'title', 'url']


class ClassroomTemplateDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    project_templates = ProjectTemplateClassroomSerializer(many=True)
    helpful_resources = HelpfulResourceSerializer(many=True)
    managers = ClassroomTemplateManagerSerializer(many=True)

    def update(self, instance, validated_data):
        project_templates_data = validated_data.pop('project_templates', [])
        helpful_resources_data = validated_data.pop('helpful_resources', [])
        managers_data = validated_data.pop('managers', [])
        instance = super().update(instance, validated_data)

        # Handle project templates
        for project_template_data in project_templates_data:
            project_template_id = project_template_data.get('id', None)
            project_template = instance.project_templates.get(id=project_template_id)
            project_template_serializer = ProjectTemplateClassroomSerializer(project_template,
                                                                             data=project_template_data,
                                                                             partial=True)
            if project_template_serializer.is_valid():
                project_template_serializer.save()

        # Handle helpful resources
        for resource_data in helpful_resources_data:
            resource_id = resource_data.get('id', None)
            if resource_id:
                resource_instance = HelpfulResource.objects.get(id=resource_id)
                for key, value in resource_data.items():
                    setattr(resource_instance, key, value)
                resource_instance.save()
            else:
                resource_data['classroom_template'] = instance
                HelpfulResource.objects.create(**resource_data)

        # Handle managers
        for manager_data in managers_data:
            manager_id = manager_data.get('id', None)
            if manager_id:
                manager_instance = ClassroomTemplateManager.objects.get(id=manager_id)
                manager_user_data = manager_data.pop('user', {})
                for key, value in manager_data.items():
                    setattr(manager_instance, key, value)
                manager_instance.save()
                user_instance = manager_instance.user
                for key, value in manager_user_data.items():
                    setattr(user_instance, key, value)
                user_instance.save()
            else:
                user = User.objects.get(username=manager_data['user']['username'])
                manager_data['user'] = user
                ClassroomTemplateManager.objects.create(classroom_template=instance, **manager_data)

        return instance

    class Meta:
        model = ClassroomTemplate
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'project_templates', 'helpful_resources',
                  'managers']


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