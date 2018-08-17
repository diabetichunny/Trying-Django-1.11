from django.core.exceptions import ValidationError

CATEGORIES = ['Pizza', 'Asian', 'American', 'Italian']


def validate_category(value):
    if value.capitalize() not in CATEGORIES:
        raise ValidationError(f'{value} is not a valid category.')
