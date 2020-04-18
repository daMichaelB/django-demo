"""
Forms can reside anywhere in your Django project. The convention is to place them inside a forms.py file
for each application.
"""
from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
