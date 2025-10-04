from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    Tests CRUD, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        """
        Prepare test data and authentication setup.
        Runs before every test.
        """
        
        self.user = User.objects.create_user(username='testuser', password='testpass')

       
        self.author = Author.objects.create(name="George Orwell")
        self.book1 = Book.objects.create(title="1984", publication_year=1949, author=self.author)
        self.book2 = Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author)

        
        self.client = APIClient()
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')


    def test_list_books(self):
        """Test retrieving all books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_unauthenticated(self):
        """Ensure unauthenticated users cannot create a book."""
        data = {"title": "Homage to Catalonia", "publication_year": 1938, "author": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Ensure authenticated users can create a book."""
        self.client.login(username='testuser', password='testpass')
        data = {"title": "Homage to Catalonia", "publication_year": 1938, "author": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book_authenticated(self):
        """Ensure authenticated users can update a book."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-update', args=[self.book1.id])
        data = {"title": "Nineteen Eighty-Four", "publication_year": 1949, "author": self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Nineteen Eighty-Four")

    def test_delete_book_authenticated(self):
        """Ensure authenticated users can delete a book."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

 
    def test_filter_books_by_title(self):
        """Filter books by title."""
        response = self.client.get(f"{self.list_url}?title=1984")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "1984")

    def test_search_books_by_author_name(self):
        """Search books by author name."""
        response = self.client.get(f"{self.list_url}?search=George")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("1984" in book['title'] for book in response.data))

    def test_order_books_by_publication_year(self):
        """Order books by publication year descending."""
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "1984")
