from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('book_list', views.list_books(), name='books'),
    path('library_details', views.LibraryDetailView.as_view(), name='details'),
]
