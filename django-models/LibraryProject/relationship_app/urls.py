from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    path('book_list', views.list_books, name='books'),
    path('library_details', views.LibraryDetailView.as_view(), name='details'),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin/dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian/dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member/dashboard/', views.member_view, name='member_dashboard'),
]
