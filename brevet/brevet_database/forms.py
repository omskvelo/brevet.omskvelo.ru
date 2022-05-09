import re

from django import forms

result_pattern = [
    re.compile("^\d\d.\d\d$"),
    re.compile("^\d\d\d\d$"),
    re.compile("^\d.\d\d$"),
    re.compile("^\d\d\d$"),
    ]

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
            if result_pattern[0].match(data['result']):
                data['result'] = data['result'][0:2] + ":" + data['result'][3:] + ":00"
            elif result_pattern[1].match(data['result']):
                data['result'] = data['result'][0:2] + ":" + data['result'][2:] + ":00"
            elif result_pattern[2].match(data['result']):
                data['result'] = '0' + data['result'][0] + ":" + data['result'][2:] + ":00"
            elif result_pattern[3].match(data['result']):
                data['result'] = '0' + data['result'][0] + ":" + data['result'][1:] + ":00"
        super().__init__(data, *args, **kwargs)