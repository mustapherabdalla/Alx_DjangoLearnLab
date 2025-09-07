from django import forms
from .models import Book, Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order authors by name
        self.fields['author'].queryset = Author.objects.all().order_by('name')
