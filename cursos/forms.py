from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import RegexValidator

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    cpf = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF inválido. Use o formato XXX.XXX.XXX-XX.')]
    )

    class Meta:
        model = Profile
        fields = ['photo', 'cpf']


