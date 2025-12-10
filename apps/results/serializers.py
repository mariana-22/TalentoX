from rest_framework import serializers
from .models import Result, UserScore

class ResultSerializer(serializers.ModelSerializer):
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    assessment_difficulty = serializers.IntegerField(source='assessment.difficulty', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Result
        fields = [
            'id', 'user', 'username', 'assessment', 'assessment_title', 
            'assessment_difficulty', 'score', 'correct_answers', 
            'total_questions', 'time_taken', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['user', 'assessment', 'correct_answers', 'total_questions', 'time_taken']
    
    def create(self, validated_data):
        result = Result.objects.create(**validated_data)
        result.calculate_score()
        result.save()
        
        # Actualizar puntaje global del usuario
        user_score, created = UserScore.objects.get_or_create(user=result.user)
        user_score.update_global_score()
        
        return result


class UserScoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    accuracy_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = UserScore
        fields = [
            'id', 'user', 'username', 'global_score', 'total_assessments',
            'total_correct', 'total_questions', 'accuracy_percentage',
            'strengths', 'weaknesses', 'recommendations', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']
    
    def get_accuracy_percentage(self, obj):
        if obj.total_questions > 0:
            return round((obj.total_correct / obj.total_questions) * 100, 2)
        return 0


class UserStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas del usuario"""
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    total_assessments = serializers.IntegerField()
    average_score = serializers.FloatField()
    best_score = serializers.FloatField()
    worst_score = serializers.FloatField()
    total_time = serializers.IntegerField()
    average_time = serializers.FloatField()
