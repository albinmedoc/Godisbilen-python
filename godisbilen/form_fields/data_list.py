from wtforms import StringField
from wtforms.widgets import TextInput, HTMLString

class DatalistInput(TextInput):
    """
    Custom widget to create an input with a datalist attribute
    """

    def __init__(self, datalist=""):
        super(DatalistInput, self).__init__()
        self.datalist = datalist

    def __call__(self, field, **kwargs):
        kwargs.setdefault("type", self.input_type)
        if(field.flags.required):
            kwargs.setdefault("required", True)

        html = [u'<datalist id="{}_list">'.format(field.id)]

        for item in field.datalist:
            html.append(u'<option value="{}">'.format(item))

        html.append(u'</datalist>')
        if(field.data is None):
            field.data = ""
        html.append(u'<input list="{}_list" {}>'.format(field.id, self.html_params(**kwargs)))

        return HTMLString(u''.join(html))


class DatalistField(StringField):
    """
    Custom field type for datalist input
    """
    widget = DatalistInput()

    def __init__(self, label=None, datalist="", validators=None, **kwargs):
        super(DatalistField, self).__init__(label, validators, **kwargs)
        self.datalist = datalist

    def _value(self):
        if self.data:
            return u''.join(self.data)
        else:
            return u''