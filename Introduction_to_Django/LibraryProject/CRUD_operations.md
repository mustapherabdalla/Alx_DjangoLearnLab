# Creation of a book instance and save it in the database.
from bookshelf.models import Book

book = Book(title="1984", author="George Orwell", publication_year=1949)

book.save()

print(book.title)

Output: 1984

# Retrieve all the book instances saved in the database.
books = Book.objects.all()

for book in books:
    print(book.title, " ", book.author, " ", book.publication_year)

Output: 1984  George Orwell  1949


# Update a book instance and save it in the database.
book = Book.objects.get(title="1984")

book.title = “Nineteen Eighty-Four”

book.save()

print(book.title)

Output: Nineteen Eighty-Four


# Delete a book instance from the database.
book = Book.objects.get(title="1984")

book.title = “Nineteen Eighty-Four”

print(book.title)

Book object (None)
