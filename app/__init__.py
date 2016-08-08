from flask import Flask, request, jsonify
from functools import wraps
app = Flask(__name__)


##################################
#
# Class / Constant Vars
#
##################################
allowed_payment_schedules = ['weekly', 'biweekly', 'monthly']
min_amortization = 5
max_amortization = 25
mortgate_interest_rate = 0.025
max_insurable_mortgage = 1000000


###################################
#
# Helper functions
#
###################################
def return_error(message, code=400):
	response = {}
	response['error'] = message
	response = jsonify(response)
	response.status_code = code
	return response


def is_down_payment_valid(asking_price, down_payment):
	if(asking_price > 500000):
		min_down_payment = 25000 + (asking_price - 500000)*0.1
	else:
		min_down_payment = asking_price*0.05
	return down_payment >= min_down_payment


def calculate_insurance(asking_price, down_payment):
	ratio = down_payment / asking_price
	if(ratio < 0.1):
		return 3.15
	if(ratio < 0.15):
		return 2.4
	if(ratio < 20):
		return 1.8
	return 0

def is_int(value):
	try:
		int(value);
	except(ValueError):
		return False
	return True

###################################
#
# Validation functions
#
###################################
def asking_price_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		asking_price = request.args.get('asking_price')
		if(asking_price):
			if(not is_int(asking_price)):
				return_error('asking_price must be an int', 400)
		
			return f(*args, **kwargs)
		return return_error('missing parameter asking_price', 400)
	return decorated_function
	
	
def down_payment_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		down_payment = request.args.get('down_payment')
		asking_price = request.args.get('asking_price')
		if(down_payment):
			if(not is_int(down_payment)):
				return_error('down_payment must be an int', 400)
			if(not is_int(asking_price)):
				return_error('asking_price must be an int', 400)

			if(is_down_payment_valid(int(asking_price), int(down_payment))):
				return f(*args, **kwargs)
			return return_error('invalid down payment: Rrequired 5% of first $500K and 10% all above', 400)

		return return_error('missing parameter down_payment', 400)
	return decorated_function
		

def payment_schedule_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		payment_schedule =  request.args.get('payment_schedule')
		if(payment_schedule):
			if(payment_schedule in allowed_payment_schedules):
				return f(*args, **kwargs)
			
			error_string = 'invalid payment schedule; must be one of: '
			error_string = error_string + ', '.join(allowed_payment_schedules)
			return return_error(error_string, 400)
		return return_error('missing parameter payment_schedule', 400)
	return decorated_function

	
def amortization_period_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		amortization_period = request.args.get('amortization_period')
		if(amortization_period):
			if(not is_int(amortization_period)):
				return return_error('amortization period must be an int', 400)

			amortization_period_int = int(amortization_period)
			if(min_amortization <= amortization_period_int <= max_amortization):
					return f(*args, **kwargs)
			return return_error('invalid amortization period; must be between ' + str(min_amortization) + ' and ' + str(max_amortization) + ' (years)', 400)
		return return_error('missing parameter amortization_period', 400)
	return decorated_function




######################################
#
# Routes
#
######################################
@app.route('/rate')
@asking_price_required
@down_payment_required
@payment_schedule_required
@amortization_period_required
def calculate_mortgage():
	down_payment = int(request.args.get('down_payment'))
	asking_price = int(request.args.get('asking_price'))
	payment_schedule =  request.args.get('payment_schedule')
	amortization_period = int(request.args.get('amortization_period'))

	insurance_cost = calculate_insurance(asking_price, down_payment)
	loan = asking_price - down_payment

	if(insurance_cost > 0.0):
		if(loan > max_insurable_mortgage):
			return return_error('your down payment requires mortgage insurance which is not avalible for this request', 200)
		loan = loan * (1 + (insurance_cost / 100) )

	if(payment_schedule == 'weekly'):
		number_of_payments = amortization_period * 52.1429
		interest_rate = mortgate_interest_rate / 52.1429
	elif(payment_schedule == 'biweekly'):
		number_of_payments = amortization_period * 26.07145
		interest_rate = mortgate_interest_rate / 26.07145
	elif(payment_schedule == 'monthly'):
		number_of_payments = amortization_period * 12
		interest_rate = mortgate_interest_rate / 12

	numerator = interest_rate*( (1+interest_rate)**number_of_payments) 
	demoninator = ((1 + interest_rate)**number_of_payments) -1
	payment = loan * ( numerator / demoninator )
	payment = format(payment, '.2f')

	response = {}
	response[payment_schedule + ' Payment'] = payment
	return	jsonify(response)

if __name__ == "__main__":
    app.run()
