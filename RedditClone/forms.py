from django import forms
from django.core import validators
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput())

class PostForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    text = forms.CharField(label='text', max_length=1000)
    link = forms.CharField(label='link', max_length=200)

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='confirm password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )