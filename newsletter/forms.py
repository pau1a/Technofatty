from django import forms

from .copy import get_copy


class NewsletterSubscribeForm(forms.Form):
    copy = get_copy()

    email = forms.EmailField(
        error_messages={
            "required": copy["required_email"],
            "invalid": copy["invalid_email"],
        }
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        data = self.cleaned_data.get("website", "")
        if data:
            raise forms.ValidationError("spam")
        return data
