from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', include('apps.users.urls')),  # Dashboard URLs
    path('students/', include('apps.students.urls')),  # Students app URLs
    path('companies/', include('apps.companies.urls')),  # Companies app URLs
    path('agreements/', include('apps.agreements.urls')),  # Agreements app URLs
    path('hours_records/', include('apps.hours_records.urls')),  # Hours Records app URLs
    path('evaluations/', include('apps.evaluations.urls')),  # Evaluations app URLs
]
