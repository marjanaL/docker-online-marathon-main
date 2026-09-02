from django import forms
from .models import Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic']
        labels = {
            'name': "Ім'я:",
            'surname': "Прізвище:",
            'patronymic': "По батькові:",
        }

        widgets = {
            'name': forms.TextInput(),
            'surname': forms.TextInput(),
            'patronymic': forms.TextInput(),
        }
