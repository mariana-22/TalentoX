from rest_framework import serializers
from .models import Certification


class CertificationSerializer(serializers.ModelSerializer):
    """Serializer completo para Certification"""
    username = serializers.CharField(source='user.username', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Certification
        fields = [
            'id', 'certificate_id', 'user', 'username', 'title', 'description',
            'level', 'level_display', 'total_score', 'assessments_completed',
            'evidence_links', 'status', 'status_display', 'is_valid',
            'issued_at', 'expires_at', 'updated_at'
        ]
        read_only_fields = ['id', 'certificate_id', 'issued_at', 'updated_at']
    
    def get_is_valid(self, obj):
        return obj.is_valid()


class CertificationCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear certificaciones"""
    class Meta:
        model = Certification
        fields = ['user', 'title', 'description', 'total_score', 
                  'assessments_completed', 'evidence_links', 'expires_at']
    
    def create(self, validated_data):
        certification = Certification.objects.create(**validated_data)
        certification.calculate_level()
        certification.save()
        return certification


class CertificationGenerateSerializer(serializers.Serializer):
    """Serializer para generar certificaciones basadas en resultados del usuario"""
    title = serializers.CharField(max_length=200, help_text="Título de la certificación")
    description = serializers.CharField(required=False, allow_blank=True, help_text="Descripción opcional")
    evidence_links = serializers.CharField(required=False, allow_blank=True, help_text="Enlaces a evidencias (JSON)")
    expires_at = serializers.DateTimeField(required=False, allow_null=True, help_text="Fecha de expiración opcional")


class CertificationHistorySerializer(serializers.ModelSerializer):
    """Serializer simplificado para historial de certificaciones"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Certification
        fields = [
            'id', 'certificate_id', 'title', 'level', 'level_display',
            'total_score', 'status', 'status_display', 'issued_at', 'expires_at'
        ]
        read_only_fields = fields
