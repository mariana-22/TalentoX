from django.db import models
from django.contrib.auth import get_user_model
from apps.skills.models import Skill

User = get_user_model()

class Evidence(models.Model):
    user = models.ForeignKey(User, related_name='evidences', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='evidences', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    external_link = models.URLField(blank=True, null=True)
    code_snippet = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class MediaFile(models.Model):
    evidence = models.ForeignKey(Evidence, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='evidence_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.evidence.title}"
