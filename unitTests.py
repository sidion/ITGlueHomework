import unittest
import json
from app import app

class MortgageCalculatorTestCase(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()

	def tearDown(self):
		pass


	###########################################
	#
	# Test to make sure all params are required
	#
	###########################################
	def test_asking_price_params_missing(self):
		rv = self.app.get('/rate?down_payment=1&payment_schedule=weekly&amortization_period=5')
		assert 'missing parameter asking_price' in rv.data




	def test_down_payment_missing(self):
		rv = self.app.get('/rate?asking_price=1&payment_schedule=weekly&amortization_period=5')
		assert 'missing parameter down_payment' in rv.data




	def test_payment_schedule_missing(self):
		rv = self.app.get('/rate?asking_price=1&down_payment=1&amortization_period=5')
		assert 'missing parameter payment_schedule' in rv.data




	def test_amortization_period_missing(self):
		rv = self.app.get('/rate?asking_price=1&down_payment=1&payment_schedule=weekly')
		assert 'missing parameter amortization_period' in rv.data


	#########################################
	#
	# Test to make sure all params are validated
	#
	#########################################
	def test_payment_schedule_valid(self):
		rv = self.app.get('/rate?asking_price=1&down_payment=1&payment_schedule=INVALID	&amortization_period=5')
		assert 'invalid payment schedule; must be one of: weekly, biweekly, monthly' in rv.data

	


	def test_amortization_period_valid(self):
		rv = self.app.get('/rate?asking_price=1&down_payment=1&payment_schedule=weekly&amortization_period=1')
		assert 'invalid amortization period; must be between 5 and 25 (years)' in rv.data
		rv = self.app.get('/rate?asking_price=1&down_payment=1&payment_schedule=weekly&amortization_period=100')
		assert 'invalid amortization period; must be between 5 and 25 (years)' in rv.data


	def test_down_payment_valid(self):
		rv = self.app.get('/rate?asking_price=750000&down_payment=1&payment_schedule=weekly&amortization_period=5')
		assert 'invalid down payment: Rrequired 5% of first $500K and 10% all above' in rv.data




	###########################################
	#
	# Verifiy use cases
	#
	###########################################
	def test_over_million_under_20_down(self):
		rv = self.app.get('/rate?asking_price=1200000&down_payment=100000&payment_schedule=weekly&amortization_period=10')
		assert 'your down payment requires mortgage insurance which is not avalible for this request' in rv.data

	def test_weekly_payment(self):
		rv = self.app.get('/rate?asking_price=750000&down_payment=75000&payment_schedule=weekly&amortization_period=5')
		assert 'weekly Payment' in rv.data
		assert '2841.62' in rv.data

	def test_biweekly_payment(self):
		rv = self.app.get('/rate?asking_price=500000&down_payment=50000&payment_schedule=biweekly&amortization_period=25')
		assert 'biweekly Payment' in rv.data
		assert '958.07' in rv.data

	def test_monthly_payment(self):
		rv = self.app.get('/rate?asking_price=500000&down_payment=100000&payment_schedule=monthly&amortization_period=25')
		assert 'monthly Payment' in rv.data
		assert '1850.99' in rv.data

if __name__ == '__main__':
    unittest.main()

