from rest_framework import serializers
from .models import Evidence, MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'file', 'uploaded_at']

class EvidenceSerializer(serializers.ModelSerializer):
    files = MediaFileSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Evidence
        fields = ['id', 'user', 'skill', 'title', 'description', 'external_link', 'code_snippet', 'created_at', 'files', 'uploaded_files']

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        evidence = Evidence.objects.create(**validated_data)
        for file in uploaded_files:
            MediaFile.objects.create(evidence=evidence, file=file)
        return evidence
