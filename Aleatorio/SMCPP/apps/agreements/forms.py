from django import forms
from django.core.exceptions import ValidationError
from .models import Agreement, Student, Company

class AgreementForm(forms.ModelForm):
    class Meta:
        model = Agreement
        fields = ['number', 'start_date', 'end_date', 'hours_required', 'status', 'student', 'company']
        labels = {
            'number': 'Número de Convenio',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha de Fin',
            'hours_required': 'Horas Requeridas',
            'status': 'Estado del Convenio',
            'student': 'Estudiante Asignado',
            'company': 'Empresa Asignada',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # ✅ AQUÍ LA REGLA DE NEGOCIO PROGRAMADA AL 100%
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        status_actual = cleaned_data.get('status')

        # Estados que consideramos como "ACTIVOS"
        estados_activos = ['IN_PROGRESS', 'EXECUTION'] 

        # Solo validamos si el estado nuevo es activo
        if status_actual in estados_activos:
            # Buscamos si el estudiante ya tiene otro convenio activo
            convenios_activos = Agreement.objects.filter(
                student=student,
                status__in=estados_activos
            )

            # Si es un convenio NUEVO y ya tiene activo: ERROR
            if self.instance.pk is None and convenios_activos.exists():
                raise ValidationError("❌ ERROR: Este estudiante ya tiene un convenio en trámite o ejecución. No puede tener dos activos a la vez.")

            # Si estamos EDITANDO y tiene otro activo distinto al que estamos editando: ERROR
            if self.instance.pk is not None:
                if convenios_activos.exclude(pk=self.instance.pk).exists():
                    raise ValidationError("❌ ERROR: Este estudiante ya tiene otro convenio activo registrado.")

        return cleaned_data