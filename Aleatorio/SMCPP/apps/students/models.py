from django.db import models
from apps.users.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    program = models.CharField(max_length=100, verbose_name="Carrera / Programa")
    cycle = models.CharField(max_length=20, verbose_name="Ciclo Académico")
    personal_data = models.TextField(verbose_name="Datos Personales")
    contact_info = models.TextField(verbose_name="Información de Contacto")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        app_label = 'apps_students' 