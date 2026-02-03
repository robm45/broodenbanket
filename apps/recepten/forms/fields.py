# forms/fields.py (of in je forms.py)

import datetime
from django import forms
from django.core.exceptions import ValidationError


class MinutenDurationField(forms.Field):
    """
    Accepteert:
    - MM
    - HH:MM
    - HH:MM:SS
    """
    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, datetime.timedelta):
            return value

        try:
            parts = value.split(":")
            parts = [int(p) for p in parts]

            if len(parts) == 1:
                minutes = parts[0]
                return datetime.timedelta(minutes=minutes)

            if len(parts) == 2:
                hours, minutes = parts
                return datetime.timedelta(hours=hours, minutes=minutes)

            if len(parts) == 3:
                hours, minutes, seconds = parts
                return datetime.timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds
                )

        except (ValueError, TypeError):
            pass

        raise ValidationError(
            "Gebruik MM of HH:MM (bijv. 30 of 01:15)"
        )

