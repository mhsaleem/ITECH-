from django import forms
from models import Title


class PunForm(forms.Form):
    puntext = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control",

            'id': 'punBody',
            'placeholder': 'Insert your pun here...',
            'rows': '5',

            'style': 'resize: vertical;'}
    ), required=True)

    tags = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'tokenfield',
            'placeholder': 'Insert tags...',
            'style': 'width: 100%;'
        }
    ), required=False)
    NSFW = forms.BooleanField(required=False)
    flagCount = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'search-query form-control',
            'name': 'q',
            'placeholder': 'Search punny..'
        }
    ), max_length=100)


class SettingsForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    title = forms.ChoiceField(required=False, choices=[(t.title, t.title) for t in Title.objects.all()])
    picture = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SettingsForm, self).__init__(*args, **kwargs)
        # self.fields['title'].choices = [(t.title, t.title) for t in Title.objects.filter(user=self.user)]
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
