from django.shortcuts import render, get_object_or_404
from django.views.generic import LastView, DetailView
from .models import Book, Library


def list_books(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(sel):
        return Library.objects.prefetch_related('books__author')
    
