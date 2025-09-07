from django.urls import path
from . import views

urlpatterns = [
    path('book_list', views.list_books, name='books'),
    path('library_details', views.LibraryDetailView.as_view(), name='details'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]
