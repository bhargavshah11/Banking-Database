import unittest
from App.analytics import update
import json

"""
Raise a value error if the Account ID provided by the user is:
    1. is not found in the Database
    2. More features can be added --> Checking for strings/alphabets in account ID. 
"""


class TestInfoUpdate(unittest.TestCase):

    def test_invalid_account(self):
        with open("record.json") as json_file:
            json_data = json.load(json_file)

            self.assertRaises(ValueError, update, "record.json")
