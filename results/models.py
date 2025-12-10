from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Result(models.Model):
    """Resultado de una evaluación completada por un usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    assessment = models.ForeignKey('Assessments.Assessment', on_delete=models.CASCADE, related_name='results')
    
    score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Puntaje del 0 al 100"
    )
    correct_answers = models.IntegerField(default=0, help_text="Cantidad de respuestas correctas")
    total_questions = models.IntegerField(default=0, help_text="Total de preguntas")
    time_taken = models.IntegerField(default=0, help_text="Tiempo tomado en segundos")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Resultado'
        verbose_name_plural = 'Resultados'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['assessment', '-score']),
        ]

    def __str__(self):
        return f"{self.user} - {self.assessment.title} - {self.score}%"
    
    def calculate_score(self):
        """Calcula el puntaje porcentual"""
        if self.total_questions > 0:
            self.score = (self.correct_answers / self.total_questions) * 100
        return self.score


class UserScore(models.Model):
    """Puntaje global y análisis del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_score')
    
    global_score = models.FloatField(default=0, help_text="Promedio global del usuario")
    total_assessments = models.IntegerField(default=0, help_text="Total de evaluaciones completadas")
    total_correct = models.IntegerField(default=0, help_text="Total de respuestas correctas")
    total_questions = models.IntegerField(default=0, help_text="Total de preguntas respondidas")
    
    strengths = models.TextField(null=True, blank=True, help_text="Fortalezas del usuario")
    weaknesses = models.TextField(null=True, blank=True, help_text="Áreas de mejora")
    recommendations = models.TextField(null=True, blank=True, help_text="Recomendaciones")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Puntaje de Usuario'
        verbose_name_plural = 'Puntajes de Usuarios'

    def __str__(self):
        return f"Score de {self.user.username}: {self.global_score}%"
    
    def update_global_score(self):
        """Actualiza el puntaje global basado en todos los resultados"""
        results = Result.objects.filter(user=self.user)
        if results.exists():
            self.total_assessments = results.count()
            self.total_correct = sum(r.correct_answers for r in results)
            self.total_questions = sum(r.total_questions for r in results)
            
            if self.total_questions > 0:
                self.global_score = (self.total_correct / self.total_questions) * 100
            
            self.save()
        return self.global_score
