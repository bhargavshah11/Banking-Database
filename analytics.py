import pymysql
import pymysql.cursors
import json


# -------- Connection to the Database ---------

connection = pymysql.connect(host='127.0.0.1',
							 user='root',
							 password='password',
							 db = 'banking',
							 charset='utf8mb4')


# -------- Assuming this is the JSON record received from Bank's API Endpoint ---------

json_data = {
			"account_id" : 1454581, 
			"event_date": "2018-01-09", 
			"account_standing": "B", 
			"account_information": {
			"first_name": "Jane", 
			"last_name": "Smith", 
			"date_of_birth": "1975-09-09", 
			"address": {
			"street_number": "345", 
			"street_name": "Oak Drive", 
			"unit_number": "12A", 
			"city": "Mount Pleasant", 
			"state": "CA", 
			"zip_code": "90010"}, 
			"email_address": "hello@yahoo.com"} 
			}


# -------- Updating database if changes found in JSON record---------

def update_email():

	# Account ID from json record
	account_check = json_data["account_id"]

	# Email ID from json record
	email_check = json_data["account_information"]["email_address"]

	try:
		with connection.cursor() as cursor:

			cursor.execute("SELECT account_id FROM clients")

			row = cursor.fetchone()

			for i in row:			
				
				# Validating account ID with existing database
				if row[0] == account_check:

					# Update email address in database
					sql = "UPDATE clients SET email_address = %s WHERE account_id = %s"

					cursor.execute(sql, (email_check, account_check))

					# Necessary to commit since it's not auto update. 
					connection.commit()

				else:

					# For similar email update request from the user
					return "It's already up-to-date"

		with connection.cursor() as cursor:

			cursor.execute("SELECT email_address FROM clients")

			row = cursor.fetchone()

			print("Email address updated successfully to:", row[0])		

	finally:
		cursor.close()
		connection.close()

if __name__ == '__main__':
	update_email()