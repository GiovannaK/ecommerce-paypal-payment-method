from django.template import Library
from utils import utils


register = Library()


@register.filter
def cart_total_qt(cart):
    return utils.cart_total_qt(cart)