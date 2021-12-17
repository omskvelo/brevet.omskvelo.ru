from django import forms

class ProtocolUploadForm(forms.Form):
    xls = forms.FileField(label="*.xls")