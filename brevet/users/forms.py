from django import forms
from django.contrib.auth.forms import UserCreationForm

from phonenumber_field.formfields import PhoneNumberField

from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=30, required=True, help_text='Необходимо для регистрации в АСР.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Необходимо для регистрации в ACP.')
    phone_number = PhoneNumberField(region='RU', help_text = 'Телефон для связи с организатором.')


    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

class SignUpVkForm(forms.Form):
    phone_number = PhoneNumberField(region='RU', help_text = 'Телефон для связи с организатором.')

