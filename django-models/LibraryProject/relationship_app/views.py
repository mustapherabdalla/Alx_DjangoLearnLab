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
class RegisterView(CreateView):
    """Class-based view for user registration"""
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('library_detail.html')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Automatically log in the user after registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, f'Account created successfully! Welcome {username}!')
        return response


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
