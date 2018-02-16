import unittest
from analytics import update
import json

######
# Raise a value error if the email Id provided by the user is invalid
######

class testInfoUpdate(unittest.TestCase):
	def test_invalid_email(self):
		
		with open("record.json") as json_file:
			json_data = json.load(json_file)		
			
			self.assertRaises(ValueError, update, "record.json")