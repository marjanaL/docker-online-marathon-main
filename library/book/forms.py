from django import forms
from .models import Book
from author.models import Author

class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        label="Оберіть автора(ів):",
        help_text="Утримуйте Ctrl, щоб обрати кількох."
    )

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
        labels = {
            'name': 'Назва книги:',
            'description': 'Опис книги:',
            'count': 'Кількість екземплярів:',
        }
