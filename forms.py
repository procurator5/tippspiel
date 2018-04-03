from django import forms

class SearchForm(forms.Form):
    quote=forms.CharField()
    