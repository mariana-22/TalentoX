"""
Models for users app.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    """
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('empresa', 'Empresa'),
        ('aprendiz', 'Aprendiz'),
    )
    
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='aprendiz',
        verbose_name='Rol'
    )
    phone = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        validators=[RegexValidator(
            regex=r'^\d{10}$',
            message="El número de teléfono debe tener exactamente 10 dígitos."
        )],
        verbose_name='Teléfono'
    )
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Profile(models.Model):
    """
    User Profile model - OneToOne relationship with User.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='Usuario'
    )
    bio = models.TextField(blank=True, null=True, verbose_name='Biografía')
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name='Avatar'
    )
    birth_date = models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ubicación')
    website = models.URLField(blank=True, null=True, verbose_name='Sitio web')
    linkedin = models.URLField(blank=True, null=True, verbose_name='LinkedIn')
    github = models.URLField(blank=True, null=True, verbose_name='GitHub')
    
    # Professional info
    current_position = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='Posición actual'
    )
    years_experience = models.PositiveIntegerField(
        default=0,
        verbose_name='Años de experiencia'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"