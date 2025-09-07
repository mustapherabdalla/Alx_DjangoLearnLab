from django.contrib import admin
from .models import Book, Author, Library, Librarian
from .models import UserProfile

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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'get_username']
    list_filter = ['role']
    search_fields = ['user__username']

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Librarian, LibrarianAdmin)
