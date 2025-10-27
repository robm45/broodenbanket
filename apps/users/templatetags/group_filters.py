from django import template

register = template.Library()

@register.filter
def in_group(user, group_name):
    """Check of de gebruiker in een bepaalde groep zit"""
    return user.groups.filter(name=group_name).exists()

