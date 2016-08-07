import unittest
import json
from app import app

class MortgageCalculatorTestCase(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()

	def tearDown(self):
		pass

	def test_params_verified(self):
		rv = self.app.get('/rate')
		assert 'missing parameter' in rv.data

if __name__ == '__main__':
    unittest.main()

