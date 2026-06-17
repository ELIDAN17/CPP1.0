from django.db import models
from apps.students.models import Student
from apps.companies.models import Company

class Agreement(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Borrador'),
        ('IN_PROGRESS', 'En Trámite'),
        ('EXECUTION', 'En Ejecución'),
        ('COMPLETED', 'Finalizado'),
        ('CANCELLED', 'Cancelado'),
    ]
    number = models.CharField(max_length=50, unique=True, verbose_name="Número de Convenio")
    start_date = models.DateField(verbose_name="Fecha de Inicio")
    end_date = models.DateField(verbose_name="Fecha de Fin")
    hours_required = models.IntegerField(verbose_name="Horas Requeridas")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='agreements')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='agreements')

    def __str__(self):
        return f"Convenio {self.number} - {self.student}"

    class Meta:
        app_label = 'apps_agreements'