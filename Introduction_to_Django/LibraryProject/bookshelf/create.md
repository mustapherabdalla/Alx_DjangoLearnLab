# Create a book instance and save it in the database.

# The below statement imports the Book model from models.py in the bookshelf app
from bookshelf.models import Book

# The below python command creates a book instance.
book = Book(title="1984", author="George Orwell", publication_year=1949)

# The below python command saves the book instance in the database.
book.save()

# The print command below prints the book title.
print(book.title)
