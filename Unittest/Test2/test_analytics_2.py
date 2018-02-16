import unittest
from analytics import update
import json

"""
Raise a Type error if the ADDRESS provided by the user:
	1. Has string instead of integers for e.g. "street_number" = "asdf"
	2. Has Empty fields
"""

class testInfoUpdate(unittest.TestCase):
	def test_invalid_address(self):	
		
		with open("record.json") as json_file:
			json_data = json.load(json_file)		
			
			self.assertRaises(ValueError, update, "record.json")
			