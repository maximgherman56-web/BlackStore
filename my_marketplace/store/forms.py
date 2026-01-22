from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order, User

# Форма оформлення замовлення (ВОНА ВЖЕ БУЛА)
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Іван'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Петренко'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380...'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Місто, вулиця...'}),
        }

# НОВА ФОРМА РЕЄСТРАЦІЇ (УКРАЇНІЗОВАНА)
class RegistrationForm(UserCreationForm):
    is_seller = forms.BooleanField(required=False, label="Я хочу продавати товари")

    class Meta:
        model = User
        fields = ['username', 'email', 'is_seller']
    
    # Цей блок замінює англійські назви на українські
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Логін (ім'я користувача)"
        self.fields['email'].label = "Електронна пошта"
        self.fields['username'].help_text = "" # Прибираємо довгу підказку англійською