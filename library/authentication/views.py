from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser
from .decorator import librarian_required
from .forms import UserRegistrationForm, UserEditForm

FIRST_NAME_LENGTH = 20
LAST_NAME_LENGTH = 20
MIDDLE_NAME_LENGTH = 20
EMAIL_LENGTH = 100

def register_view(request):
    """Registration of a new user (visitor or librarian)."""
    if request.user.is_authenticated:

        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Реєстрація пройшла успішно! Тепер ви можете увійти.")

                return redirect('login')
            except Exception:
                messages.error(request, "Виникла помилка під час створення акаунту.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
  

@librarian_required
def edit_user_view(request, user_id):
    """Update/PUT functionality for editing an existing user."""
    target_user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Дані користувача {target_user.email} успішно оновлено!")
            return redirect('user_detail', user_id=target_user.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Помилка у полі {field}: {error}")
    else:
        form = UserEditForm(instance=target_user)

    return render(request, 'edit_user.html', {'form': form, 'target_user': target_user})


def login_view(request):
    """Login."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Раді бачити вас знову, {user.first_name}!")

                return redirect('home')
            else:
                messages.error(request, "Ваш акаунт деактивовано.")
        else:
            messages.error(request, "Невірний Email або пароль.")

    return render(request, 'login.html')


def logout_view(request):
    """Logout."""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Ви успішно вийшли з системи.")

    return redirect('home')


@librarian_required
def all_users_view(request):
    """Showing information about all users"""
    users = CustomUser.objects.all()
    
    return render(request, 'all_users.html', {'users': users})


@librarian_required
def user_detail_view(request, user_id):
    """Showing details of a specific user by ID."""
    target_user = CustomUser.get_by_id(user_id)
    if not target_user:
        messages.error(request, "Користувача з таким ID не знайдено.")

        return redirect('all_users')

    return render(request, 'authentication/user_detail.html', {'target_user': target_user})
