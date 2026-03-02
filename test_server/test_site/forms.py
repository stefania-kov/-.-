from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application
import re

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин (латиница и цифры, мин. 6 символов)'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        })
    )
    
    fio = forms.CharField(
        label='ФИО',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов Иван Иванович'
        })
    )
    
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '8(XXX)XXX-XX-XX'
        })
    )
    
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль (мин. 8 символов)'
        })
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'fio', 'phone', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем стандартные подсказки Django
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Переопределяем сообщения об ошибках для password2
        self.fields['password2'].error_messages = {
            'password_too_short': 'Пароль слишком короткий. Минимум 8 символов',
            'password_too_common': 'Слишком простой пароль',
            'password_entirely_numeric': 'Пароль не может состоять только из цифр',
            'password_mismatch': 'Пароли не совпадают',
        }
    
    # ВАЖНО: переопределяем метод, который проверяет password2
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password1 or not password2:
            raise forms.ValidationError('Введите пароль')
        
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        
        # Проверка длины
        if len(password2) < 8:
            raise forms.ValidationError('Пароль должен быть минимум 8 символов')
        
        # Проверка на простые пароли
        if password2.isdigit():
            raise forms.ValidationError('Пароль не может состоять только из цифр')
        
        common_passwords = ['password', '12345678', 'qwerty', 'password123']
        if password2.lower() in common_passwords:
            raise forms.ValidationError('Слишком простой пароль')
        
        return password2
    
    # Остальные проверки
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 6:
            raise forms.ValidationError('Логин должен быть не менее 6 символов')
        if not re.match('^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('Только латинские буквы и цифры')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже существует')
        return username
    
    def clean_fio(self):
        fio = self.cleaned_data['fio']
        if not re.match('^[а-яА-ЯёЁ ]+$', fio):
            raise forms.ValidationError('Только кириллица и пробелы')
        return fio
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
            raise forms.ValidationError('Формат: 8(XXX)XXX-XX-XX')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже зарегистрирован')
        return email

class ApplicationForm(forms.ModelForm):
    start_date = forms.DateField(
        label='Желаемая дата начала',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'ДД.ММ.ГГГГ'
        })
    )
    
    class Meta:
        model = Application
        fields = ['course', 'start_date', 'payment_method']
        labels = {
            'course': 'Курс',
            'payment_method': 'Способ оплаты',
        }
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()