from .models import Book, Library

# Query all books by a specific author
# noinspection PyUnresolvedReferences
author_books = Book.objects.get(author="George Orwell")

# List all the books in a library
# noinspection PyUnresolvedReferences
library = Library.objects.get(name=library_name)
books = library.books.all()

# Retrieve the librarian for a library
# noinspection PyUnresolvedReferences
librarian = Library.objects.get(library="MTL")


