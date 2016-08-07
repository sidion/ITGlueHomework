from flask import Flask, request, jsonify
from functools import wraps
app = Flask(__name__)


def asking_price_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if( request.args.get('asking_price') ):
			return f(*args, **kwargs)
		response = {}
		response['error'] = 'missing parameter asking_price'
		response = jsonify(response)
		response.status_code = 400
		return response
	return decorated_function
		

@app.route('/')
def hello():
	return 'hello'

@app.route('/rate')
@asking_price_required
def calculate_mortgage():
	return 0

if __name__ == "__main__":
    app.run()
