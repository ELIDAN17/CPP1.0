from django.urls import path
from . import views  # Import the views from the current directory

urlpatterns = [
    path('list/', views.list_view, name='list'),  # List view URL
    path('detail/<int:id>/', views.detail_view, name='detail'),  # Detail view URL with an id parameter
    path('create/', views.create_view, name='create'),  # Create view URL
    path('update/<int:id>/', views.update_view, name='update'),  # Update view URL with an id parameter
    path('delete/<int:id>/', views.delete_view, name='delete'),  # Delete view URL with an id parameter
]
