from django.db import models
from apps.agreements.models import Agreement
from apps.users.models import User

class HourRecord(models.Model):
    date = models.DateField(verbose_name="Fecha")
    hours = models.IntegerField(verbose_name="Cantidad de Horas")
    activity_description = models.TextField(verbose_name="Descripción de Actividad")
    evidence = models.FileField(upload_to='evidence/', null=True, blank=True, verbose_name="Evidencia")
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name='hours_records')
    tutor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'MENTOR'})
    approved = models.BooleanField(default=False, verbose_name="¿Aprobado?")

    def __str__(self):
        return f"{self.date} - {self.hours} horas"

    class Meta:
        app_label = 'apps_hours_records'