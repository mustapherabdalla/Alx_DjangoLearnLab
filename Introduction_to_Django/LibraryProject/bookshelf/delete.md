# Delete a book instance and save in the database.

# The below statement imports the Book model from models.py in the bookshelf app
from bookshelf.models import Book

# The below python command fetches the book instance using its title.
book = Book.objects.get(title="1984")

# The below python command deletes the book from the database.
book.delete()

# The print command below prints the book title after deletion.
print(book.title)

# The expected output of the above command is:
Book object (None)
