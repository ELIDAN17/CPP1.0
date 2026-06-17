from django import forms
from .models import HourRecord, Agreement, User

class HoursRecordForm(forms.ModelForm):
    class Meta:
        model = HourRecord
        fields = ['date', 'hours', 'activity_description', 'evidence', 'agreement', 'tutor', 'approved']
        labels = {
            'date': 'Fecha de Registro',
            'hours': 'Cantidad de Horas',
            'activity_description': 'Descripción de la Actividad Realizada',
            'evidence': 'Archivo / Evidencia de Trabajo',
            'agreement': 'Convenio Relacionado',
            'tutor': 'Tutor Responsable',
            'approved': '¿Aprobado?',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'activity_description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Detalle qué actividades realizó...'}),
        }

    # Filtramos para que solo aparezcan convenios que están en ejecución
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agreement'].queryset = Agreement.objects.filter(status='EXECUTION')
        self.fields['tutor'].queryset = User.objects.filter(role='MENTOR')