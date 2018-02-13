import pymysql
import pymysql.cursors
import json
import re

# -------- Connection to the Database ------------------------------------------------

connection = pymysql.connect(host='127.0.0.1',
							 user='root',
							 password='pwd',   #Enter your sql db password here
							 db = 'banking',           #Enter your db name here
							 charset='utf8mb4')


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

	# Email ID from json record (info received from bank's API end point)
	email_id_update = json_data["account_information"]["email_address"]

	# Email address validation using Regex 
	if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_id_update) != None:
		return True

	# Raise error: If email couldn't pass through the regex email validation 
	raise ValueError("Email address entered is Invalid")
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

		# View after the user has successfully updated the Email ID
		sql = "SELECT concat(first_name,' ', last_name) FROM update_info"

		cnx.execute(sql)
		
		client_name = cnx.fetchone()

		print("Hi " + client_name[0] + "!")

		sql = "SELECT email_address FROM update_info"

		cnx.execute(sql)

		clients_email = cnx.fetchone()

		print("Your email address has been updated to: " + clients_email[0])

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

		sql = """
			UPDATE clients 
			SET street_number = %s, street_name = %s, unit_number = %s, city = %s, state = %s, zip_code = %s  
			WHERE account_id = %s """
		
		cnx.execute(sql, (street_num_update, street_name_update, unit_num_update, city_update, state_update, zip_update, account_id_check))  
		
		# Commit all updates (It's not auto_commit by default) 
		connection.commit()

		# View after the user has successfully updated the Address

		sql = "SELECT concat(street_number,' ',street_name,' ',unit_number,' ',city,' ',state,' ',zip_code) FROM update_info"

		cnx.execute(sql)

		clients_address = cnx.fetchone()

		print("Address is:", clients_address[0])

	except:
		# Raise type error if string is entered instead of int for INT fields in the address 
		raise TypeError("Address entered is invalid or has empty fields")
		return False

# -------- Main function that executes only if account ID is validated ----------------

#####
# 	Assuming that user may change their "email ID" as well as their "address".
# 	Either Way, we're trying to update everything to keep it simple (having time constraints) 
# 	Many features can be added. This is the most basic form of programming. 
#####

def update(filename):
	
	# Opening JSON file (Assuming we're receiving that from BANK's API End-point)
	with open(filename) as json_file:
		json_data = json.load(json_file)

	# Account ID from json record
	account_id_check = json_data["account_id"]

	try:
		with connection.cursor() as cnx:
				
			rows = validate_account(json_data, cnx)
			
			# Execute the validate methos only if account_ID is found in the database
			if rows != None:

				if validate_email(json_data):
					update_email(json_data, cnx)
					update_address(json_data, cnx)
					
			else:
				# Raise error if the account number entered by the user is not in DB 
				raise ValueError("Account number entered is invalid")

	finally:
		cnx.close()
		connection.close()

if __name__ == '__main__':
	update("record.json")
