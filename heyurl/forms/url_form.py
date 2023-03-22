from django import forms


class UrlForm(forms.Form):
    original_url = forms.CharField(label='Original URL', max_length=255, required=True,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': "form-control",
                                           'placeholder': 'http://www.example.com'
                                       }
                                   ))
