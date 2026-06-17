# ⚠️ ESTAS SON LAS LÍNEAS QUE FALTABAN, YA LAS PUSE
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum  # Necesario para sumar horas
from .models import HoursRecord, Agreement
from .forms import HoursRecordForm  # Este lo crearemos en el siguiente paso

def create_hours_record(request):
    # Validar que el convenio esté en estado de Ejecución
    agreement = get_object_or_404(Agreement, id=request.POST.get('agreement'), status='En ejecución')
    
    if request.method == 'POST':
        form = HoursRecordForm(request.POST)
        if form.is_valid():
            hours_record = form.save(commit=False)
            hours_record.save()
            
            # Si se aprueba, se actualiza el total (lógica que funciona)
            if hours_record.approved:
                # Podemos agregar lógica extra aquí si es necesario
                pass
            return redirect('hours_records:list')  # Redirección corregida con nombre de ruta
    else:
        form = HoursRecordForm()
    
    return render(request, 'hours_records/create.html', {'form': form})

# ✅ ALGORITMO 1: Cálculo de horas totales APROBADAS
def calculate_total_hours(agreement_id):
    agreement = get_object_or_404(Agreement, id=agreement_id)
    total_hours = agreement.hoursrecord_set.filter(approved=True).aggregate(total=Sum('hours'))['total'] or 0
    return total_hours

# ✅ ALGORITMO 2: Cálculo de horas que faltan
def calculate_remaining_hours(min_required, total_hours):
    if min_required <= 0:
        return 0
    remaining_hours = min_required - total_hours
    return remaining_hours if remaining_hours > 0 else 0


# --- AQUÍ AGREGAMOS LAS FUNCIONES QUE FALTABAN (list, update, delete, approve) ---

def list_view(request):
    # Muestra lista de registros, filtra según rol (lo completamos)
    records = HoursRecord.objects.all().order_by('-date')
    return render(request, 'hours_records/list.html', {'records': records})

def detail_view(request, id):
    record = get_object_or_404(HoursRecord, id=id)
    return render(request, 'hours_records/detail.html', {'record': record})

def update_view(request, id):
    record = get_object_or_404(HoursRecord, id=id)
    if request.method == 'POST':
        form = HoursRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('hours_records:list')
    else:
        form = HoursRecordForm(instance=record)
    return render(request, 'hours_records/create.html', {'form': form})

def delete_view(request, id):
    record = get_object_or_404(HoursRecord, id=id)
    record.delete()
    return redirect('hours_records:list')

# ✅ FUNCIÓN ESPECIAL: APROBAR HORAS (Solo para Tutor)
def approve_hours(request, id):
    record = get_object_or_404(HoursRecord, id=id)
    record.approved = True
    record.save()
    return redirect('hours_records:list')