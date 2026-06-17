from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('COORDINATOR', 'Coordinador'),
        ('MENTOR', 'Tutor'),
        ('STUDENT', 'Estudiante'),
    ]
    role = models.CharField(max_length=15, choices=ROLES, default='STUDENT')

    class Meta:
        app_label = 'apps_users'