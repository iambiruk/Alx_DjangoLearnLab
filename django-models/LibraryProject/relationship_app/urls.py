from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'relationship_app'
["views.register", "LogoutView.as_view(template_name=", "LoginView.as_view(template_name="]


urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Protected content URLs
    path('', views.home_view, name='home'),
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
]
