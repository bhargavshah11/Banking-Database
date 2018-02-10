import pymysql
import pymysql.cursors
import json
import re

# -------- Connection to the Database ------------------------------------------------

connection = pymysql.connect(host='127.0.0.1',
							 user='root',
							 password='pwd',   		   #Enter your sql db password here
							 db = 'banking',           #Enter your db name here
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
				"email_address": "ads@yahoo.com"} 
			}

# -------------------------------- Validating Account ID ----------------------------
def validate_account(json_data, cnx):

	# Account ID from json record
	account_id_check = json_data["account_id"]

	try:

		# Check for user requested account ID from database 
		sql = "SELECT account_id FROM clients WHERE account_id = %s"
		cnx.execute(sql, account_id_check)

		rows = cnx.fetchone()

		return rows

	except:
		return False

# -------------------------------- Validating Email ID ------------------------------

def validate_email(json_data):

	# Email ID from json record
	email_id_update = json_data["account_information"]["email_address"]

	# Email address validation
	if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_id_update) != None:
		return True

	print("Email address entered is Invalid")
	return False

# -------- Updating Email ID in the Database -----------------------------------

def update_email(json_data, cnx):

	# Account ID from json record
	account_id_check = json_data["account_id"]

	# Email ID from json record
	email_id_update = json_data["account_information"]["email_address"]
	try:

		# Update email address in database
		sql = "UPDATE clients SET email_address = %s WHERE account_id = %s"
		cnx.execute(sql, (email_id_update, account_id_check))

		# Necessary to commit since it's not auto update. 
		connection.commit()

		cnx.execute("SELECT * FROM clients WHERE account_id = %s", account_id_check)

		row = cnx

	except:
		return False

# -------- Updating Address in the Database -------------------------------------

def update_address(json_data, cnx):

	# Account ID from json record
	account_id_check = json_data["account_id"]

	street_num_update = json_data["account_information"]["address"]["street_number"]
	street_name_update = json_data["account_information"]["address"]["street_name"]
	unit_num_update = json_data["account_information"]["address"]["unit_number"]
	city_update = json_data["account_information"]["address"]["city"]
	state_update = json_data["account_information"]["address"]["state"]
	zip_update = json_data["account_information"]["address"]["zip_code"]

	try:   
		rows = validate_account(json_data)

		sql = """
			UPDATE clients 
			SET street_number = %s, street_name = %s, unit_number = %s, city = %s, state = %s, zip_code = %s  
			WHERE account_id = %s """
		
		cnx.execute(sql, (street_num_update, street_name_update, unit_num_update, city_update, state_update, zip_update, account_id_check))  

		connection.commit()

	except:
		return False

# -------- Main function that executes only if account ID is validated ----------------

def update(json_data):

	# Account ID from json record
	account_id_check = json_data["account_id"]

	try:
		with connection.cursor() as cnx:
	
			rows = validate_account(json_data, cnx)
		
			if rows != None:
				
				if validate_email(json_data):
					update_email(json_data, cnx)
					update_address(json_data, cnx)

					sql = "SELECT * FROM clients WHERE account_id = %s"
					
					cnx.execute(sql, account_id_check)

					row = cnx.fetchone()

					print(row)

			else:
				print("Sorry! Your account doesn't exist.")

	finally:
		cnx.close()
		connection.close()

if __name__ == '__main__':
	update(json_data)