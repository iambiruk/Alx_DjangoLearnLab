from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

def list_all_books(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library'] = Library.objects.prefetch_related('books__author').get(pk=self.object.pk)
        return context