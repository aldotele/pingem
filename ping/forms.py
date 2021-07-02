from django import forms
from ping.models import Url


class UrlForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Enter Url'}), label=False, max_length=1024)
    regexp = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter regexp (optional)'}),
                             label=False, max_length=1024, required=False)

    class Meta:
        model = Url
        fields = ['link', 'regexp']
