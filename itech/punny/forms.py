from django import forms


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
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'form-control',
        }
    ))
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'form-control'
        }
    ))
    title = forms.ChoiceField(widget=forms.Select(
        attrs={
            'class' : 'form-control'
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class' : 'form-control',
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class' : 'form-control',
        }
    ))
    # def clean(self):
    #     if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
    #





