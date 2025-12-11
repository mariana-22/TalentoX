"""
Models for organizations app.
"""
from django.db import models
from django.core.validators import RegexValidator
from apps.users.models import User


class Organization(models.Model):
    """
    Organization model representing companies.
    """
    name = models.CharField(max_length=200, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
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
    website = models.URLField(blank=True, null=True, verbose_name='Sitio web')
    logo = models.ImageField(upload_to='organizations/logos/', blank=True, null=True, verbose_name='Logo')
    
    # Address information
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ciudad')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='País')
    
    # Business information
    industry = models.CharField(max_length=100, blank=True, null=True, verbose_name='Industria')
    size = models.CharField(
        max_length=20,
        choices=[
            ('small', '1-50 empleados'),
            ('medium', '51-200 empleados'),
            ('large', '201-1000 empleados'),
            ('enterprise', '1000+ empleados'),
        ],
        default='small',
        verbose_name='Tamaño'
    )
    
    # Relationships
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_organizations',
        limit_choices_to={'role': 'empresa'},
        verbose_name='Propietario'
    )
    administrators = models.ManyToManyField(
        User,
        related_name='administered_organizations',
        blank=True,
        verbose_name='Administradores'
    )
    
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Organización'
        verbose_name_plural = 'Organizaciones'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def total_members(self):
        """Returns total number of members in all teams."""
        return User.objects.filter(team_members__organization=self).distinct().count()
    
    @property
    def total_teams(self):
        """Returns total number of teams."""
        return self.teams.count()


class Team(models.Model):
    """
    Team model representing work groups within organizations.
    ManyToMany relationship with Users.
    """
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='teams',
        verbose_name='Organización'
    )
    
    members = models.ManyToManyField(
        User,
        related_name='team_members',
        blank=True,
        verbose_name='Miembros'
    )
    
    team_lead = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_teams',
        verbose_name='Líder del equipo'
    )
    
    # Team information
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='Departamento')
    project = models.CharField(max_length=200, blank=True, null=True, verbose_name='Proyecto')
    
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['-created_at']
        unique_together = ['organization', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.organization.name}"
    
    @property
    def member_count(self):
        """Returns the number of members in the team."""
        return self.members.count()