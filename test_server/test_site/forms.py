from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application
import re

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'fio', 'phone']
    # 1. ТУТ МЕНЯЕМ ПОДПИСИ И ПЛЕЙСХОЛДЕРЫ
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Русские названия полей
        self.fields['username'].label = 'Логин'
        self.fields['email'].label = 'Email'
        self.fields['fio'].label = 'ФИО'
        self.fields['phone'].label = 'Телефон'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        # Плейсхолдеры (подсказки внутри полей)
        self.fields['username'].widget.attrs['placeholder'] = 'Логин (латиница и цифры, мин. 6 символов)'
        self.fields['email'].widget.attrs['placeholder'] = 'example@mail.com'
        self.fields['fio'].widget.attrs['placeholder'] = 'Иванов Иван Иванович'
        self.fields['phone'].widget.attrs['placeholder'] = '8(XXX)XXX-XX-XX'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль (мин. 8 символов)'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        # Bootstrap классы для красоты
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    # 2. ТУТ ПИШЕМ ПРОВЕРКИ (валидацию)
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 6:
            raise forms.ValidationError('Логин должен быть не менее 6 символов')
        if not re.match('^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('Только латинские буквы и цифры')
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
    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен быть минимум 8 символов')
        return password

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