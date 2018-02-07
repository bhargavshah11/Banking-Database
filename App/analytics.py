import pymysql
import pymysql.cursors
import json
import re 


# -------- Connection to the Database ------------------------------------------------

connection = pymysql.connect(host='127.0.0.1',
			     user='root',
			     password='pwd',   #Enter your sql db password here
			     db = 'banking',   #Enter your db name here
			     charset='utf8mb4')


# -------- Assuming this is the JSON record received from Bank's API Endpoint ---------

json_data = {
		"account_id" : 1454582, 
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
		"email_address": "jsmith@yahoo.com"} 
	   }


# -------- Updating database if changes found in JSON record ----------------------------

def update_email():

	# Account ID from json record
	account_id_check = json_data["account_id"]

	# Email ID from json record
	email_id_update = json_data["account_information"]["email_address"]

	try:
		with connection.cursor() as cursor:			
			
			# Check for user requested account ID from database 
			sql = "SELECT account_id FROM clients WHERE account_id = %s"
			cursor.execute(sql, account_id_check)
			
			rows = cursor.fetchone()

			# Executes when account Id is found in DB.
			if rows != None:
				# Email address validation
				if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_id_update) != None:
				
					# Update email address in database
					sql = "UPDATE clients SET email_address = %s WHERE account_id = %s"
					cursor.execute(sql, (email_id_update, account_id_check))

					# Necessary to commit since it's not auto update. 
					connection.commit()

					print("Email address has been updated to:", email_id_update)

				else:
					print("Email address entered is Invalid")

			else:
				print("Sorry! Your account doesn't exist.")

	finally:
		cursor.close()
		connection.close()

if __name__ == '__main__':
	update_email()
