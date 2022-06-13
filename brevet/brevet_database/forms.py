import re

from django import forms

result_pattern = re.compile("^(\d{1,2})[^\d]?(\d{2})$")

class ProtocolUploadForm(forms.Form):
    xls = forms.FileField(label="*.xls")


class AddResultForm(forms.Form):
    """ Add result form for manual result calculation (deprecated). Note field types."""
    result = forms.DurationField()
    medal = forms.BooleanField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        """ Allows user to enter time in HH[?]MM format instead of default HH:MM:SS format.
        Any delimiter is valid.
        """
        if data:
            data = data.copy()
            result = data['result'].strip()
            result_match = result_pattern.match(result)
            if result_match:
                data['result'] = result_match.group(1) + ":" + result_match.group(2) + ":00"

            print (data['result'])

        super().__init__(data, *args, **kwargs)


class AddResultTimeForm(forms.Form):
    """ Add result form for automatic result calculation. Note field types."""
    result = forms.TimeField()
    medal = forms.BooleanField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        """ Allows user to enter time in HH[?]MM format instead of default HH:MM:SS format.
        Any delimiter is valid.
        """
        if data:
            data = data.copy()
            result = data['result'].strip()
            result_match = result_pattern.match(result)
            if result_match:
                data['result'] = result_match.group(1) + ":" + result_match.group(2) + ":00"

            print (data['result'])

        super().__init__(data, *args, **kwargs)