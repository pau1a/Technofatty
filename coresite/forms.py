from django import forms
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name (Optional)',
            'autocomplete': 'name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email',
            'required': True,
        })
    )
    company = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Company (Optional)',
            'autocomplete': 'organization',
        })
    )
    hp_field = forms.CharField(required=False, widget=forms.HiddenInput())
    consent = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the privacy policy to subscribe.'})

    def clean_hp_field(self):
        """Check that the honeypot field is empty."""
        if self.cleaned_data.get('hp_field'):
            raise ValidationError('This form was submitted by a bot.', code='honeypot')
        return ''