from django.urls import path
from . import views

urlpatterns = [
    path('book_list', views.book_list, name='books'),
    path('library_details', views.LibraryDetails.as_view(), name='details'),
]
