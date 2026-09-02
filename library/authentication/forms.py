from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        label="Пароль:"
    )
    
    ROLE_CHOICES = [
        ('0', 'Звичайний користувач (Гість)'),
        ('1', 'Бібліотекар (Адміністратор)'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'auth-select'}),
        label="Оберіть роль у системі:"
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'last_name', 'first_name', 'middle_name', 'role']
        labels = {
            'email': 'Email (Логін):',
            'last_name': 'Прізвище:',
            'first_name': "Ім'я:",
            'middle_name': 'По батькові:',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким Email вже зареєстрований.")
        
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()

        return user


class UserEditForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('0', 'Звичайний користувач'),
        ('1', 'Бібліотекар'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'auth-select'}),
        label="Роль у системі:"
    )

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'middle_name', 'role']
        labels = {
            'last_name': 'Прізвище:',
            'first_name': "Ім'я:",
            'middle_name': 'По батькові:',
        }
