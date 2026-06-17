from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    ROLES = (
        ('ESTUDIANTE', 'Estudiante'),
        ('TUTOR', 'Tutor Empresarial'),
        ('COORDINADOR', 'Coordinador de Prácticas'),
        ('ADMINISTRADOR', 'Administrador'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')
    dni = models.CharField(max_length=8, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"