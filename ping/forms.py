from django import forms
from ping.models import Url


class UrlForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Enter Url', 'style': 'width: 350px;'}),
                         label=False, max_length=2048)
    regexp = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter regex (optional)',
                                                           'style': 'width: 180px;'}),
                             label=False, max_length=1024, required=False)

    class Meta:
        model = Url
        fields = ['link', 'regexp']
