from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import admin_required, librarian_required, member_required
from .decorators import is_admin, is_librarian, is_member
from django.contrib.auth.decorators import permission_required

# Create your views here.
class LibraryDetailView(ListView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_queryset(self):
        library = Library.objects.get(name="MTL")
        return library

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library'] = self.get_queryset()
        return context


def list_books(request):
    books = Book.objects.all()

    return render(request, 'relationship_app/list_books.html', {
        'books': books,
        'can_add': request.user.has_perm('relationship_app.can_add_book')
    })


# Add Book View (requires permission)
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book (requires can_add_book permission)"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('relationship_app:book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()

    return render(request, 'relationship_app/book_form.html', {
        'form': form,
        'title': 'Add New Book'
    })


# Edit Book View (requires permission)
@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """View to edit an existing book (requires can_change_book permission)"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('relationship_app:book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)

    return render(request, 'relationship_app/book_form.html', {
        'form': form,
        'title': f'Edit Book: {book.title}',
        'book': book
    })


# Delete Book View (requires permission)
@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book (requires can_delete_book permission)"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('relationship_app:book_list')

    return render(request, 'relationship_app/book_confirm_delete.html', {
        'book': book
    })


# Book Detail View (requires view permission)
@login_required
@permission_required('relationship_app.can_view_book', raise_exception=True)
def book_detail(request, pk):
    """View book details (requires can_view_book permission)"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/book_detail.html', {
        'book': book,
        'can_edit': request.user.has_perm('relationship_app.can_change_book'),
        'can_delete': request.user.has_perm('relationship_app.can_delete_book')
    })


# Function-based login view
def login_view(request):
    """Function-based view for user login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Redirect to next page if provided, otherwise home
                next_page = request.GET.get('library_detail.html')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'relationship_app/login.html', {'form': form})


# Logout view
def logout_view(request):
    """Function-based view for user logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('relationship_app/login.html')


# Admin View - Using decorator from decorators.py
@admin_required
def admin_view(request):
    """View accessible only to Admin users"""
    context = {
        'user': request.user,
        'role': request.user.profile.get_role_display(),
        'total_users': User.objects.count(),
        'total_libraries': Library.objects.count(),
        'total_books': Book.objects.count(),
    }
    return render(request, 'relationship_app/admin_view.html', context)


# Librarian View - Using user_passes_test decorator
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users"""
    # Get libraries managed by this librarian
    try:
        librarian = Librarian.objects.get(name=request.user.username)
        managed_library = librarian.library
        books_count = managed_library.books.count()
    except Librarian.DoesNotExist:
        managed_library = None
        books_count = 0

    context = {
        'user': request.user,
        'role': request.user.profile.get_role_display(),
        'managed_library': managed_library,
        'books_count': books_count,
    }
    return render(request, 'relationship_app/librarian_view.html', context)


# Member View - Using decorator from decorators.py
@member_required
def member_view(request):
    """View accessible only to Member users"""
    # Get all libraries and books for members to browse
    libraries = Library.objects.all()
    books = Book.objects.all().select_related('author')

    context = {
        'user': request.user,
        'role': request.user.profile.get_role_display(),
        'libraries_count': libraries.count(),
        'books_count': books.count(),
        'recent_books': books.order_by('-id')[:5],  # Show 5 most recent books
    }
    return render(request, 'relationship_app/member_view.html', context)


# Update registration view to set default role
def register(request):
    """Function-based view for user registration with role assignment"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Set user role (default to 'member')
            user.profile.role = 'member'
            user.profile.save()

            # Automatically log in the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Account created successfully! Welcome {username}!')
                return redirect('relationship_app:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


@login_required
def profile_view(request):
    """View for user profile with role information"""
    user = request.user
    role_display = user.profile.get_role_display() if hasattr(user, 'profile') else 'No role assigned'

    return render(request, 'relationship_app/profile.html', {
        'user': user,
        'role': role_display
    })
