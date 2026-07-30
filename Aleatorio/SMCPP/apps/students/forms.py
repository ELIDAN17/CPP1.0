from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'program', 'cycle', 'personal_data', 'contact_info']
        labels = {
            'user': 'Usuario Asociado',
            'program': 'Carrera / Programa',
            'cycle': 'Ciclo Académico',
            'personal_data': 'Datos Personales',
            'contact_info': 'Información de Contacto',
        }
        widgets = {
            'personal_data': forms.Textarea(attrs={'rows': 3}),
            'contact_info': forms.Textarea(attrs={'rows': 3}),
        }