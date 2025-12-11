from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

User = get_user_model()


class Certification(models.Model):
    """Certificaciones basadas en evidencias, resultados y nivel del usuario"""
    
    LEVEL_CHOICES = [
        (0, 'Sin Certificar'),
        (1, 'Novato'),
        (2, 'Aprendiz'),
        (3, 'Competente'),
        (4, 'Avanzado'),
        (5, 'Experto'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('active', 'Activa'),
        ('expired', 'Expirada'),
        ('revoked', 'Revocada'),
    ]
    
    # Identificador único de la certificación
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Usuario que recibe la certificación
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    
    # Información de la certificación
    title = models.CharField(max_length=200, help_text="Título de la certificación")
    description = models.TextField(null=True, blank=True, help_text="Descripción de la certificación")
    
    # Nivel de habilidad certificado (0-5 según escala TalentoX)
    level = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=LEVEL_CHOICES,
        help_text="Nivel de habilidad certificado"
    )
    
    # Puntaje total obtenido
    total_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Puntaje total obtenido (0-100)"
    )
    
    # Evaluaciones asociadas (referencia a resultados)
    assessments_completed = models.IntegerField(default=0, help_text="Número de evaluaciones completadas")
    
    # Evidencias asociadas (URL o referencia)
    evidence_links = models.TextField(null=True, blank=True, help_text="Enlaces a evidencias (JSON)")
    
    # Estado de la certificación
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Fechas
    issued_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de emisión")
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Fecha de expiración")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issued_at']
        verbose_name = 'Certificación'
        verbose_name_plural = 'Certificaciones'
        indexes = [
            models.Index(fields=['user', '-issued_at']),
            models.Index(fields=['status', '-issued_at']),
            models.Index(fields=['level', '-total_score']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username} (Nivel {self.level})"
    
    def calculate_level(self):
        """Calcula el nivel basado en el puntaje total"""
        if self.total_score >= 90:
            self.level = 5  # Experto
        elif self.total_score >= 75:
            self.level = 4  # Avanzado
        elif self.total_score >= 60:
            self.level = 3  # Competente
        elif self.total_score >= 40:
            self.level = 2  # Aprendiz
        elif self.total_score >= 20:
            self.level = 1  # Novato
        else:
            self.level = 0  # Sin Certificar
        return self.level
    
    def is_valid(self):
        """Verifica si la certificación está activa y vigente"""
        from django.utils import timezone
        if self.status != 'active':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
