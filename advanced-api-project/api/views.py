from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class BookListView(generics.ListAPIVIEW):
    """
    ListView: Retrives all books.
    Accessible by anyone (Read-Only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView: Retrives a single book by ID.
    Accessible by anyone (Read-Only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreteAPIView):
    """
    CreateView: Allows authenticated users to add a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Hook: Add extra logic when creating a book.
        Example: You could attach the request user as metadata.
        """
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Allows authenticated users to modify a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes =[permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Hook: Add custom behaviour on update.
        Example: Logging updates, enforcing business rules, etc,
        """
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Allows authenticated users to remove a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

