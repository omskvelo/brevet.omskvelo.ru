import re

from django import forms

result_pattern = re.compile("^\d\d.\d\d$")
result_pattern_no_delimiter = re.compile("^\d\d\d\d$")

class ProtocolUploadForm(forms.Form):
    xls = forms.FileField(label="*.xls")


class AddResultForm(forms.Form):
    result = forms.DurationField()
    medal = forms.BooleanField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        """ Allows user to enter duration in HH:MM format instead of default HH:MM:SS format.
        In case user uses different symbol for ":" , the result can still be valid.
        In case user misses ":" entirely, the result can still be valid.
        """
        if data:
            data = data.copy()
            data['result'] = data['result'].strip()
            if result_pattern.match(data['result']):
                data['result'] = data['result'][0:2] + ":" + data['result'][3:] + ":00"
            if result_pattern_no_delimiter.match(data['result']):
                data['result'] = data['result'][0:2] + ":" + data['result'][2:] + ":00"

        super().__init__(data, *args, **kwargs)