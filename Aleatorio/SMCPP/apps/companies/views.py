# Importaciones que faltaban
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Company
from .forms import CompanyForm

# Listar Empresas
@login_required
def list_view(request):
    companies = Company.objects.all()
    return render(request, 'companies/list.html', {'companies': companies})

# Ver Detalle
@login_required
def detail_view(request, id):
    company = get_object_or_404(Company, id=id)
    return render(request, 'companies/detail.html', {'company': company})

# Registrar Empresa (Solo Admin/Coordinador)
@login_required
@user_passes_test(lambda u: u.rol in ['Administrador', 'Coordinador'])
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companies:list')
    else:
        form = CompanyForm()
    return render(request, 'companies/create.html', {'form': form})

# Editar Empresa
@login_required
@user_passes_test(lambda u: u.rol in ['Administrador', 'Coordinador'])
def update_view(request, id):
    company = get_object_or_404(Company, id=id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('companies:list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'companies/create.html', {'form': form})

# Eliminar Empresa
@login_required
@user_passes_test(lambda u: u.rol in ['Administrador', 'Coordinador'])
def delete_view(request, id):
    company = get_object_or_404(Company, id=id)
    company.delete()
    return redirect('companies:list')