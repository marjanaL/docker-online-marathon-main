from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Author
from .forms import AuthorForm
from authentication.decorator import librarian_required

FIRST_NAME_LENGTH = 20
LAST_NAME_LENGTH = 20
PATRONYMIC_LENGTH = 20

def home(request):
    """Home page."""

    return render(request, 'author/home.html')


@librarian_required
def librarian_dashboard(request):
    """
    Librarian dashboard for managing authors (Librarians only).
    Displays a list of all authors and handles creation of new records.
    """
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f"Автора {author.surname} успішно додано!")
            return redirect('librarian_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Помилка у полі {form.fields[field].label}: {error}")
    else:
        form = AuthorForm()
    authors = Author.objects.prefetch_related('books').all()
    context = {
        'authors': authors,
        'form': form
    }

    return render(request, 'author/librarian_dashboard.html', context)


@librarian_required
def edit_author(request, author_id):
    """
    Update/PUT functionality for editing an existing author.
    """
    author = get_object_or_404(Author, pk=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, f"Дані автора {author.surname} успішно оновлено!")
            return redirect('librarian_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Помилка: {error}")
    else:
        form = AuthorForm(instance=author)

    return render(request, 'author/edit_author.html', {'form': form, 'author': author})

@librarian_required
def delete_author(request, author_id):
    """Delete an author, only if the request is POST and there are no linked books."""
    if request.method == 'POST':
        author = get_object_or_404(Author, pk=author_id)
        if author.books.exists():
            messages.error(request, f"Неможливо видалити автора {author.surname}, оскільки до нього прив'язані книги!")
        else:
            author.delete()
            messages.success(request, f"Автор {author.surname} успішно видалений!")
            
    return redirect('librarian_dashboard')
