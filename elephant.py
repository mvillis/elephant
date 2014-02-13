from flask import Flask, render_template, request
import sys

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def order():
    order = {}
    if request.method == 'POST':
        order['discount_rate'], order['discount_price'], order['tax_rate'], order['tax_amount'], order[
            'final_price'] = run_calc(int(request.form['qty']), int(request.form['price']), request.form['state'])
    return render_template('order.html', order=order)


class StateException(Exception):
    pass


class ValueException(Exception):
    pass


taxes = {"UT": 6.85,
         "NV": 8.00,
         "TX": 6.25,
         "AL": 4.00,
         "CA": 8.25}


def validate(state):
    return state in taxes.keys()


def total(qty, price):
    return qty * price


def discount(amount):
    discount = 0
    if amount >= 1000:
        discount = .03
    if amount >= 5000:
        discount = .05
    if amount >= 7000:
        discount = .07
    if amount >= 10000:
        discount = .10
    if amount >= 50000:
        discount = .15
    return discount


def calc_tax(state, amt):
    tax_rate = taxes[state] / 100
    return tax_rate


def apply_discount(amt, dsc):
    return amt - (amt * dsc)


def run_calc(qty, price, state):
    if not validate(state):
        raise StateException()
    print "Quantity:" + str(qty)
    print "Price:" + str(price)
    print "State:" + str(state)
    amount = total(qty, price)
    print "Total:" + str(amount)
    print "Discount rate:" + str(discount(amount) * 100) + "%"
    discounted = apply_discount(amount, discount(amount))
    print "Discounted price: $" + str(discounted)
    tax_rate = calc_tax(state, discounted)
    print "Tax rate:" + str(tax_rate)
    tax = discounted * tax_rate
    print "Tax:" + str(tax)
    final_price = discounted + tax
    print "*************"
    print "Total: $%.2f" % final_price
    print "*************"
    return str(discount(amount) * 100) + "%", discounted, str(tax_rate), str(tax), final_price