from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Book, Library, UserProfile
# from .forms import CustomUserCreationForm  # Keep commented for now

# Utility functions for role checking
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_admin()

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_librarian()

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_member()

# Add the missing function
def get_user_role(user):
    if hasattr(user, 'profile'):
        return user.profile.get_role_display()
    return 'No Role'

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(LoginRequiredMixin, DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    login_url = '/relationship/login/'

    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')

# Class-based view to list all libraries
class LibraryListView(LoginRequiredMixin, ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    login_url = '/relationship/login/'

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # username field actually contains email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.email}! Your role: {get_user_role(user)}')
                next_url = request.GET.get('next', '/relationship/')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'relationship_app/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        # Use Django's built-in form temporarily
        from django.contrib.auth.forms import UserCreationForm
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Default role is 'member' as set in the model
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our library system. Your role: Member')
            return redirect('relationship_app:list_books')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        from django.contrib.auth.forms import UserCreationForm
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

@login_required(login_url='/relationship/login/')
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return render(request, 'relationship_app/logout.html')

# Protected home view
@login_required(login_url='/relationship/login/')
def home_view(request):
    user_role = get_user_role(request.user)
    return render(request, 'relationship_app/home.html', {'user_role': user_role})

# Role-Based Views
@login_required(login_url='/relationship/login/')
@user_passes_test(is_admin, login_url='/relationship/access-denied/')
def admin_view(request):
    from .models import UserProfile  # Import here to avoid circular imports
    users = UserProfile.objects.all().select_related('user')
    libraries = Library.objects.all()
    return render(request, 'relationship_app/admin_view.html', {
        'users': users,
        'libraries': libraries,
        'user_role': get_user_role(request.user)
    })

@login_required(login_url='/relationship/login/')
@user_passes_test(is_librarian, login_url='/relationship/access-denied/')
def librarian_view(request):
    # Librarians can see books and manage their library
    books = Book.objects.all().select_related('author')
    libraries = Library.objects.all()
    return render(request, 'relationship_app/librarian_view.html', {
        'books': books,
        'libraries': libraries,
        'user_role': get_user_role(request.user)
    })

@login_required(login_url='/relationship/login/')
@user_passes_test(is_member, login_url='/relationship/access-denied/')
def member_view(request):
    # Members can see available books and libraries
    books = Book.objects.all().select_related('author')
    libraries = Library.objects.all()
    return render(request, 'relationship_app/member_view.html', {
        'books': books,
        'libraries': libraries,
        'user_role': get_user_role(request.user)
    })

# Access denied view
def access_denied_view(request):
    return render(request, 'relationship_app/access_denied.html', status=403)