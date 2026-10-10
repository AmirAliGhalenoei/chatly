import re
from django.core.exceptions import ValidationError

def validate_phone_ir(phone):
    pattern = r"^09\d{9}$"
    if not re.match(pattern, phone):
        raise ValidationError("شماره تلفن نامعتبر است")
    return phone
