import unittest
from analytics_duplicate import update

"""
Raise a Type error if the ADDRESS provided by the user:
	1. Has string instead of integers for e.g. "street_number" = "asdf"
	2. Has Empty fields
"""

class testInfoUpdate(unittest.TestCase):
	def test_invalid_address(self):
		self.assertRaises(TypeError, update)