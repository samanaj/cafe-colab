from django import template

register = template.Library()

#definicion de variables para utilizar en el template
@register.filter()
def multiply(value, arg):
    return float(value) * arg

#filtro para formatear dinero, value seria el importe y arg el argumento o simbolo.
@register.filter()
def money_format(value, arg):
    return f"{value}{arg}"
