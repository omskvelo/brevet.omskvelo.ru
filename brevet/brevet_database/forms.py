import re

from django import forms

result_pattern = re.compile("^\d\d\:\d\d$")

class ProtocolUploadForm(forms.Form):
    xls = forms.FileField(label="*.xls")


class AddResultForm(forms.Form):
    result = forms.DurationField()
    medal = forms.BooleanField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        if data:
            data = data.copy()
            data['result'] = data['result'].strip()
            if result_pattern.match(data['result']):
                data['result'] += ":00"
        super().__init__(data, *args, **kwargs)