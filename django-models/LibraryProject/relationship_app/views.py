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
    template_name = 'relationship_app/list_books.html'
    context = {'books': books}

    return render(request, template_name, context)


# User Registration View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import admin_required, librarian_required, member_required
from .decorators import is_admin, is_librarian, is_member


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
