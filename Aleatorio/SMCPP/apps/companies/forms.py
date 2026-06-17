from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['business_name', 'ruc', 'address', 'representative', 'sector', 'contact_info']
        labels = {
            'business_name': 'Razón Social',
            'ruc': 'RUC / Identificación Fiscal',
            'address': 'Dirección',
            'representative': 'Representante Legal',
            'sector': 'Rubro / Actividad',
            'contact_info': 'Información de Contacto',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'contact_info': forms.Textarea(attrs={'rows': 3}),
        }