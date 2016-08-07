from flask import Flask, request, jsonify
from functools import wraps
app = Flask(__name__)

allowed_payment_schedules = ['weekly', 'biweekly', 'monthly']
min_amortization = 5
max_amortization = 25


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
			return return_error('invalid payment schedule; must be one of: weekly, biweekly, monthly', 400)
		return return_error('missing parameter payment_schedule', 400)
	return decorated_function

	
def amortization_period_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		amortization_period = request.args.get('amortization_period')
		if(amortization_period):
			if(min_amortization < amortization_period < max_amortization):
					return f(*args, **kwargs)
			return return_error('invalid amortization period; must be between 5 and 25 (years)', 400)
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
	return 0

if __name__ == "__main__":
    app.run()
