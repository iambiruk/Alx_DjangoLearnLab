import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Change to your project name if different
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing"""
    # Clear existing data
    Librarian.objects.all().delete()
    Library.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    author3 = Author.objects.create(name="Stephen King")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)
    book4 = Book.objects.create(title="The Shining", author=author3)
    book5 = Book.objects.create(title="Fire & Blood", author=author2)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Library")
    library3 = Library.objects.create(name="University Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4, book5)
    library3.books.add(book1, book4, book5)
    
    # Create librarians
    Librarian.objects.create(name="Alice Johnson", library=library1)
    Librarian.objects.create(name="Bob Smith", library=library2)
    # library3 intentionally has no librarian for testing
    
    print("Sample data created successfully!")
    return True

def query_all_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def list_all_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\nBooks in {library_name} library:")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        print(f"\nLibrarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Exception as e:
        print(f"No librarian assigned to {library_name}.")
        return None

if __name__ == "__main__":
    # Create sample data first
    create_sample_data()
    
    print("=" * 50)
    print("SAMPLE QUERIES - TASK 1 COMPLETED")
    print("=" * 50)
    
    # Query all books by a specific author
    query_all_books_by_author("J.K. Rowling")
    
    # List all books in a library
    list_all_books_in_library("Central Library")
    
    # Retrieve the librarian for a library
    retrieve_librarian_for_library("Central Library")
    
    # Additional test queries
    print("\n" + "=" * 30)
    print("ADDITIONAL TEST QUERIES")
    print("=" * 30)
    
    query_all_books_by_author("George R.R. Martin")
    list_all_books_in_library("City Library")
    retrieve_librarian_for_library("City Library")
    
    # Test case where library has no librarian
    retrieve_librarian_for_library("University Library")