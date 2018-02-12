import unittest
from analytics_duplicate import update

"""
Raise a value error if the Account ID provided by the user:
	1. is not found in the Database
	2. More features can be added --> Checking for strings/alphabets in account ID. 
"""


class testInfoUpdate(unittest.TestCase):
	def test_invalid_account(self):
		self.assertRaises(ValueError, update)