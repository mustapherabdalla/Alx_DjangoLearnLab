from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from .models import Book, Library

# Create your views here.
class LibraryDetails(ListView):
    model = Book
    template_name = "relationship_app/library_detail.html"
    context_object_name = "books"

    def get_queryset(self):
        library = Library.objects.get(name="MTL")
        return library

    def get_context_data(self, **kwargs):
        """Add library information to the context"""
        context = super().get_context_data(**kwargs)

        # Add the library object to context
        context['library'] = self.get_queryset()

        return context


def book_list(request):
    books = Book.objects.all()
    template_name = 'relationship_app/list_books.html'
    context = {'books': books}

    return render(request, template_name, context)
