import unittest
from analytics_duplicate import update

######
# Raise a value error if the email Id provided by the user is invalid
######


class testInfoUpdate(unittest.TestCase):
	def test_invalid_email(self):
		self.assertRaises(ValueError, update)