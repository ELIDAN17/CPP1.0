# Importaciones que faltaban
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages # Para mensajes de error/éxito
from .models import Agreement
from .forms import AgreementForm

# Listar Convenios
@login_required
def list_view(request):
    # Estudiante solo ve los suyos
    if request.user.rol == 'Estudiante':
        agreements = Agreement.objects.filter(student__user=request.user)
    else:
        agreements = Agreement.objects.all()
    return render(request, 'agreements/list.html', {'agreements': agreements})

# Ver Detalle
@login_required
def detail_view(request, id):
    agreement = get_object_or_404(Agreement, id=id)
    return render(request, 'agreements/detail.html', {'agreement': agreement})

# Registrar Convenio (SOLO COORDINADOR)
@login_required
@user_passes_test(lambda u: u.rol == 'Coordinador' or u.is_superuser)
def create_agreement(request):
    if request.method == 'POST':
        form = AgreementForm(request.POST)
        if form.is_valid():
            # --- ✅ AQUÍ LA REGLA DE ORO: NO 2 CONVENIOS ACTIVOS ---
            student = form.cleaned_data['student']
            existe_activo = Agreement.objects.filter(
                student=student,
                status__in=['En trámite', 'En ejecución'] # Estados que cuentan como activos
            ).exists()

            if existe_activo:
                # Si ya tiene uno, devolvemos error
                messages.error(request, '❌ ERROR: Este estudiante ya tiene un convenio activo o en trámite.')
                return render(request, 'agreements/create.html', {'form': form})
            
            # Si no tiene, guardamos
            form.save()
            messages.success(request, '✅ Convenio registrado correctamente.')
            return redirect('agreements:list')
    else:
        form = AgreementForm()
    return render(request, 'agreements/create.html', {'form': form})

# Editar Convenio y Cambiar Estado
@login_required
@user_passes_test(lambda u: u.rol == 'Coordinador' or u.is_superuser)
def update_view(request, id):
    agreement = get_object_or_404(Agreement, id=id)
    if request.method == 'POST':
        form = AgreementForm(request.POST, instance=agreement)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Convenio actualizado.')
            return redirect('agreements:list')
    else:
        form = AgreementForm(instance=agreement)
    return render(request, 'agreements/create.html', {'form': form})

# Eliminar Convenio
@login_required
@user_passes_test(lambda u: u.rol in ['Administrador', 'Coordinador'])
def delete_view(request, id):
    agreement = get_object_or_404(Agreement, id=id)
    agreement.delete()
    messages.warning(request, '🗑️ Convenio eliminado.')
    return redirect('agreements:list')

# --- ✅ FUNCIÓN ESPECIAL: CAMBIAR ESTADO ---
@login_required
@user_passes_test(lambda u: u.rol == 'Coordinador')
def change_status(request, id, new_status):
    agreement = get_object_or_404(Agreement, id=id)
    # Validamos que el cambio de estado sea lógico
    estados_permitidos = ['En trámite', 'En ejecución', 'Finalizado', 'Observado']
    if new_status in estados_permitidos:
        agreement.status = new_status
        agreement.save()
        messages.success(request, f'🔄 Estado cambiado a: {new_status}')
    return redirect('agreements:detail', id=id)