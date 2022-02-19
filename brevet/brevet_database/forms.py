from django import forms

class ProtocolUploadForm(forms.Form):
    xls = forms.FileField(label="*.xls")


class AddResultForm(forms.Form):
    result = forms.DurationField(label="Время")