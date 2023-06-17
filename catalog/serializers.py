from rest_auth import serializers

from catalog.models import ClassroomTemplate


class ClassroomTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomTemplate
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'managers']
