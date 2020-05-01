from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # add type=password to the html


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    # for all fieldnames we can define 'clean_*' functions that are evaluated by the forms 'is_valid()'
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd["password2"]:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
