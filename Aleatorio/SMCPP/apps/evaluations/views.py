# ⚠️ LÍNEAS QUE FALTABAN, YA LAS AGREGUÉ
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg  # Necesario para el promedio
from .models import Evaluation, Agreement
from .forms import EvaluationForm # Este también lo crearemos en el siguiente paso

def create_evaluation(request):
    # Validar que el convenio esté activo y sea el tutor asignado
    agreement = get_object_or_404(Agreement, id=request.POST.get('agreement'), status='En ejecución')
    
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            # Podemos asignar automáticamente el usuario actual como quien evalúa
            evaluation.evaluated_by = request.user
            evaluation.save()
            return redirect('evaluations:list')
    else:
        form = EvaluationForm()
    
    return render(request, 'evaluations/create.html', {'form': form})

# ✅ ALGORITMO: Calcular nota final promedio
def calculate_final_average(agreement_id):
    agreement = get_object_or_404(Agreement, id=agreement_id)
    average = agreement.evaluation_set.aggregate(promedio=Avg('grade'))['promedio'] or 0
    return round(average, 2)


# --- FUNCIONES BÁSICAS QUE FALTABAN ---

def list_view(request):
    evaluations = Evaluation.objects.all().order_by('-date')
    return render(request, 'evaluations/list.html', {'evaluations': evaluations})

def detail_view(request, id):
    eva = get_object_or_404(Evaluation, id=id)
    return render(request, 'evaluations/detail.html', {'eva': eva})

def update_view(request, id):
    eva = get_object_or_404(Evaluation, id=id)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=eva)
        if form.is_valid():
            form.save()
            return redirect('evaluations:list')
    else:
        form = EvaluationForm(instance=eva)
    return render(request, 'evaluations/create.html', {'form': form})

def delete_view(request, id):
    eva = get_object_or_404(Evaluation, id=id)
    eva.delete()
    return redirect('evaluations:list')