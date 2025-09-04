# Retrieve all the book instances saved in the database.

# The below statement imports the Book model from models.py in the bookshelf app
from bookshelf.models import Book

# The below python command fetches all the book instances saved in the database.
books = Book.objects.get(title="1984")

# The below python command loops through the book instances and prints their titles, authors and publication year.
for book in books:
    print(book.title, " ", book.author, " ", book.publication_year)

# The expected output of the above command is:
1984  George Orwell  1949
