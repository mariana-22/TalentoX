from rest_framework import serializers
from .models import Assessment, Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text", "is_correct"]


class OptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ["id", "text", "order", "options"]


class QuestionCreateSerializer(serializers.ModelSerializer):
    options = OptionCreateSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ["text", "order", "options"]
    
    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        
        return question


class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ["id", "title", "description", "difficulty", "time_limit", "created_at", "updated_at", "questions"]
        read_only_fields = ["id", "created_at", "updated_at"]


class AssessmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ["title", "description", "difficulty", "time_limit"]


class SubmitAnswersSerializer(serializers.Serializer):
    """Serializer para enviar múltiples respuestas"""
    question_id = serializers.IntegerField(required=True, help_text="ID de la pregunta")
    option_id = serializers.IntegerField(required=True, help_text="ID de la opción seleccionada")

