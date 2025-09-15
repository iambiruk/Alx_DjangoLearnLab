from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import models
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.html import escape
from .models import Book, Author
from .forms import BookForm, AuthorForm
from .forms import ExampleForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import BookForm

@login_required
def book_search(request):
    """
    Secure search implementation using Django ORM to prevent SQL injection.
    User input is properly handled through ORM queries.
    """
    query = request.GET.get('q', '').strip()
    
  
    if not query or len(query) > 100:
        books = Book.objects.none()
    else:
        
        books = Book.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(isbn__icontains=query)
        )[:50]  
    
    context = {
        'books': books,
        'query': escape(query),  
    }
    return render(request, 'bookshelf/book_search.html', context)
def form_example(request):
    """
    Example form view to demonstrate security features including:
    - CSRF protection
    - Form validation
    - XSS prevention
    - Input sanitization
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Security: Form validation prevents malformed data
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            return render(request, 'bookshelf/form_example.html', {
                'form': BookForm(),
                'success_message': 'Book created successfully!'
            })
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

@login_required
def book_api_search(request):
    """
    Secure API endpoint with proper input validation and output escaping.
    """
    query = request.GET.get('q', '').strip()
    
    
    if not query or len(query) > 100:
        return JsonResponse({'error': 'Invalid query'}, status=400)
    
    
    books = Book.objects.filter(
        models.Q(title__icontains=query) |
        models.Q(author__icontains=query)
    )[:10]
   
    results = [
        {
            'id': book.id,
            'title': escape(book.title),  
            'author': escape(book.author),  
            'isbn': book.isbn
        }
        for book in books
    ]
    
    return JsonResponse({'results': results})


@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """
    Secure book listing with proper permission checks.
    Uses Django ORM for safe database queries.
    """
    books = Book.objects.all().order_by('title')
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """
    Secure book creation with CSRF protection and form validation.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'action': 'Create'
    })

# Add similar security measures to all other views


