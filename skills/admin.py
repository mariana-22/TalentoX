from django.contrib import admin
from .models import Category, Skill, SkillLevel

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name","category","created_at")
    search_fields = ("name","description")

@admin.register(SkillLevel)
class SkillLevelAdmin(admin.ModelAdmin):
    list_display = ("user","skill","level","updated_at")
    list_filter = ("level",)