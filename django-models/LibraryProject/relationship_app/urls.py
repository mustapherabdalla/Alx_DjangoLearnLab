from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('book_list', views.list_books, name='books'),
    path('library_details', views.LibraryDetailView.as_view(), name='details'),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
