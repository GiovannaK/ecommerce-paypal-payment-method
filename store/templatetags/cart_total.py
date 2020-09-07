from django.template import Library
from utils import utils

register = Library()

@register.filter
def cart_totals(cart):
    return utils.cart_totals(cart)