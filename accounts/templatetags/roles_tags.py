from django import template

register = template.Library()

@register.filter
def tiene_rol(user, rol_nombre):
    return user.groups.filter(name=rol_nombre).exists()
