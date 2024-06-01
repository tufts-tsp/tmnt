from django import forms
from django.forms import ValidationError
from django.utils.safestring import mark_safe

class UploadDFDFileForm(forms.Form):
    inputText = forms.CharField(
        label=mark_safe("Paste or write your DFD code...<br />"),
        label_suffix="",
        widget=forms.Textarea(),
        required=False
    )
    inputFile = forms.FileField(
        label="Or upload a DFD file...",
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('inputText') or cleaned_data.get('inputFile')):
            raise ValidationError("Please input a DFD", code='missing_dfd')
