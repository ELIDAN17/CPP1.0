# Importaciones que faltaban
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student
from .forms import StudentForm

# Listar Estudiantes (Todos pueden ver según permiso)
@login_required
def list_view(request):
    # Si es estudiante, solo ve su ficha
    if request.user.rol == 'Estudiante':
        students = Student.objects.filter(user=request.user)
    # Admin y Coordinador ven todos
    else:
        students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

# Ver Detalle
@login_required
def detail_view(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'students/detail.html', {'student': student})

# Crear Estudiante (Admin / Coordinador)
@login_required
@user_passes_test(lambda u: u.rol in ['Administrador', 'Coordinador'])
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students:list')
    else:
        form = StudentForm()
    return render(request, 'students/create.html', {'form': form})

# Editar Estudiante
@login_required
@user_passes_test(lambda u: u.rol in ['Administrador', 'Coordinador'])
def update_view(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students:list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/create.html', {'form': form})

# Eliminar Estudiante
@login_required
@user_passes_test(lambda u: u.rol in ['Administrador', 'Coordinador'])
def delete_view(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('students:list')