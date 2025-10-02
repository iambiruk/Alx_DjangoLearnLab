from django.db import models

class Author(models.Model):
    """
    Author model: Represents an author who can write multiple books.
    Fields:
    - name: The name of the author (string).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Book(models.Model):
    """Book model: Represents a book written by an author.
    Fields
    - title: Title of the book (string).
    - publication_year: Year book was published (integer).
    - author: ForeignKey linking to Author, one author can have many books.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title
    