import re
from wtforms.validators import ValidationError

class PhoneNumber(object):

    def __init__(self, pattern, message=None):
        self.pattern = pattern
        self.message = message

    def __call__(self, form, field):
        temp = re.sub("[^0-9]", "", field.data)
        if(not re.match(self.pattern, temp)):
            raise ValidationError(self.message)