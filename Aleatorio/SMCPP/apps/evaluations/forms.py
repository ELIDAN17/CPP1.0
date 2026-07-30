from django import forms
from .models import Evaluation, Agreement, User

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['score', 'comments', 'type_of_evaluation', 'agreement', 'tutor']
        labels = {
            'score': 'Calificación / Nota (0-20)',
            'comments': 'Comentarios y Observaciones',
            'type_of_evaluation': 'Tipo de Evaluación',
            'agreement': 'Convenio Relacionado',
            'tutor': 'Tutor que Evalúa',
        }
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

    # Filtramos convenios activos y tutores
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agreement'].queryset = Agreement.objects.filter(status__in=['EXECUTION', 'COMPLETED'])
        self.fields['tutor'].queryset = User.objects.filter(role='MENTOR')