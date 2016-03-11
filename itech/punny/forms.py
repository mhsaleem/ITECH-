from django import forms
from punny.models import Pun


class PunForm(forms.Form):
    puntext = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'id': 'punBody',
            'placeholder': 'Insert your pun here..',
            'rows': '5'}
    ), required=True)
    tags = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'tokenfield',
            'placeholder': 'Insert tags..',
            'style': 'width: 100%;'
        }
    ), required=False)
    NSFW = forms.BooleanField(required=False)
    score = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    flagCount = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)

