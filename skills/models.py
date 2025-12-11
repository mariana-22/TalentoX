from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    category = models.ForeignKey(Category, related_name="skills", on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "category")

    def __str__(self):
        return self.name

class SkillLevel(models.Model):
    user = models.ForeignKey(User, related_name="skill_levels", on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name="skill_levels", on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1)  # 1..10 por ejemplo
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "skill")
        ordering = ["-level", "-updated_at"]

    def __str__(self):
        return f"{self.user} - {self.skill} ({self.level})"