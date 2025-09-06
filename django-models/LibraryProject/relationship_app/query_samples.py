import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian
def query_all_books_by_author(author_name):
    objects.filter(author=author)
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        books = author_books.all()
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return[]

def list_all_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name} library:")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}; not found.")
def retrive_librarian_for_library(library_name):
    """Retrive the librarian for a library"""
    ["Librarian.objects.get(library="]
    try:
        library = Library.objects.get(name=Library.name)
        librarian = library.librarian
        print(f"Librarian for {library_name}: {library_name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
        return None
    except Library.librarian.RelatedObjectDoesNotExist:
        print(f"No librarian assigned to {library_name} library.")
        return None
if __name__ == "__main__":
    print("=== Sample Queries ===")
    print("\n. Query all books by a specific author:")
    query_all_books_by_author("J.K. Rowling")

    print("\n2. List all books in a library:")
    list_all_books_in_library("Central Library")

    print("\n3. Retrive the librarian for a library:")

    retrive_librarian_for_library("Central Library")

