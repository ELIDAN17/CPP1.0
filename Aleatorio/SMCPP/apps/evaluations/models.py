from django.db import models
from apps.agreements.models import Agreement
from apps.users.models import User

class Evaluation(models.Model):
    TYPE_CHOICES = [
        ('PARTIAL', 'Parcial'),
        ('FINAL', 'Final'),
    ]
    score = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Calificación")
    comments = models.TextField(verbose_name="Comentarios")
    type_of_evaluation = models.CharField(max_length=20, choices=TYPE_CHOICES)
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name='evaluations')
    tutor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'MENTOR'})

    def __str__(self):
        return f"Evaluación {self.type_of_evaluation} - {self.score}"

    class Meta:
        app_label = 'apps_evaluations'