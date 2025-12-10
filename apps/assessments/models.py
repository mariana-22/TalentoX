from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Assessment(models.Model):
    """Modelo para pruebas inteligentes y retos"""
    DIFFICULTY_CHOICES = [
        (1, 'Muy Fácil'),
        (2, 'Fácil'),
        (3, 'Medio'),
        (4, 'Difícil'),
        (5, 'Muy Difícil'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    difficulty = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=DIFFICULTY_CHOICES
    )
    time_limit = models.IntegerField(default=60, help_text="Tiempo límite en segundos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'

    def __str__(self):
        return self.title


class Question(models.Model):
    """Modelo para preguntas dentro de una evaluación"""
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    order = models.IntegerField(default=1, help_text="Orden de la pregunta")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['assessment', 'order']
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        unique_together = ('assessment', 'order')

    def __str__(self):
        return f"{self.assessment.title} - P{self.order}"


class Option(models.Model):
    """Modelo para opciones de respuesta"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'

    def __str__(self):
        return f"{self.text} ({'correcta' if self.is_correct else 'incorrecta'})"
