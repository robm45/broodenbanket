from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Voeg een CSS class toe aan een form field widget."""
    return field.as_widget(attrs={"class": css_class})

