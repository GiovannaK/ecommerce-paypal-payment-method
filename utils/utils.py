"""
format the price to Real standard
"""

def formatting_price(val):
    return f'R$ {val:.2f}'.replace('.', ',')

"""
 Sum the quantity of products in the cart
"""

def cart_total_qt(cart):
    return sum([item['quantity'] for item in cart.values()])


"""
calculates the total price in the cart
"""

def cart_totals(cart):
    return sum([item.get('quantitative_price') for item in cart.values()])