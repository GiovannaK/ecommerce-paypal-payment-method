from django.template import Library

register = Library()

@register.filter
def formatting_price(val):
    return f'R$ {val:.2f}'.replace('.', ',')

    