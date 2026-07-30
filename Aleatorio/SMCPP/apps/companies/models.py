from django.db import models

class Company(models.Model):
    business_name = models.CharField(max_length=200, verbose_name="Razón Social")
    ruc = models.CharField(max_length=11, unique=True, verbose_name="RUC")
    address = models.TextField(verbose_name="Dirección")
    representative = models.CharField(max_length=150, verbose_name="Representante Legal")
    sector = models.CharField(max_length=100, verbose_name="Rubro / Actividad")
    contact_info = models.TextField(verbose_name="Información de Contacto")

    def __str__(self):
        return self.business_name

    class Meta:
        app_label = 'apps_companies'