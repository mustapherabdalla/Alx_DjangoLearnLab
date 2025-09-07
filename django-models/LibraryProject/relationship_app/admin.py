from django.contrib import admin
from .models import Book, Author, Library, Librarian

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['name']


class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author')
    search_fields = ('title', 'author')


class LibraryAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['name']


class LibrarianAdmin(admin.ModelAdmin):
    list_filter = ('name', 'library')
    search_fields = ('name', 'library')

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Librarian, LibrarianAdmin)
