from django.core.management.base import BaseCommand
from relationship_app.models import Author, Book, Library, Librarian

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        Author.objects.all().delete()
        Book.objects.all().delete()
        Library.objects.all().delete()
        Librarian.objects.all().delete()

        # Create authors
        author1 = Author.objects.create(name="J.K. Rowling")
        author2 = Author.objects.create(name="George R.R. Martin")
        author3 = Author.objects.create(name="Stephen King")

        # Create books
        books = [
            Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1),
            Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1),
            Book.objects.create(title="A Game of Thrones", author=author2),
            Book.objects.create(title="A Clash of Kings", author=author2),
            Book.objects.create(title="The Shining", author=author3),
            Book.objects.create(title="It", author=author3),
        ]

        # Create libraries
        central_lib = Library.objects.create(name="Central Library")
        city_lib = Library.objects.create(name="City Library")

        # Add books to libraries
        central_lib.books.add(books[0], books[1], books[4], books[5])
        city_lib.books.add(books[2], books[3], books[4])

        # Create librarians
        Librarian.objects.create(name="Sarah Johnson", library=central_lib)
        Librarian.objects.create(name="Michael Brown", library=city_lib)

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data'))