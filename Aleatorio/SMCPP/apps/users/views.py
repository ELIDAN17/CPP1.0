# Importaciones necesarias (faltaban antes)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import CustomUser
from .forms import UserForm, LoginForm, ProfileForm

# Vista de Inicio de Sesión
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirige al panel principal
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# Vista de Cerrar Sesión
def user_logout(request):
    auth_logout(request)
    return redirect('login')

# Registrar Usuario (SOLO ADMINISTRADOR)
@login_required
@user_passes_test(lambda u: u.is_superuser or u.rol == 'Administrador')
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:list')
    else:
        form = UserForm()
    return render(request, 'users/register.html', {'form': form})

# Listar Usuarios (SOLO ADMINISTRADOR)
@login_required
@user_passes_test(lambda u: u.is_superuser or u.rol == 'Administrador')
def list_view(request):
    users = CustomUser.objects.all()
    return render(request, 'users/list.html', {'users': users})

# Ver Detalle
@login_required
def detail_view(request, id):
    user = get_object_or_404(CustomUser, id=id)
    return render(request, 'users/detail.html', {'user': user})

# Editar Usuario
@login_required
@user_passes_test(lambda u: u.is_superuser or u.rol == 'Administrador')
def update_view(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/register.html', {'form': form})

# Eliminar Usuario
@login_required
@user_passes_test(lambda u: u.is_superuser or u.rol == 'Administrador')
def delete_view(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.delete()
    return redirect('users:list')

# Ver y Editar Perfil Propio
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})