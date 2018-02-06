import pymysql
import pymysql.cursors
import json


# -------- Connection to the Database ---------

connection = pymysql.connect(host='127.0.0.1',
							 user='root',
							 password='password',
							 db = 'banking',
							 charset='utf8mb4')
							 # cursorclass=pymysql.cursors.DictCursor)


json_data = {"account_id" : 1454581, "event_date": "2018-01-09", "account_standing": "B", "account_information": {"first_name": "Jane", "last_name": "Smith", "date_of_birth": "1975-09-09", "address": {"street_number": "345", "street_name": "Oak Drive", "unit_number": "12A", "city": "Mount Pleasant", "state": "CA", "zip_code": "90010"}, "email_address": "hello@yahoo.com"} }


# -------- Execute desired functions on the database ---------

def update_email():

	account_check = json_data["account_id"]

	email_check = json_data["account_information"]["email_address"]

	try:
		with connection.cursor() as cursor:

			cursor.execute("SELECT account_id FROM clients")

			row = cursor.fetchone()

			for i in row:			
				
				if row[0] == account_check:

					# Update email address in database
					sql = "UPDATE clients SET email_address = %s WHERE account_id = %s"

					cursor.execute(sql, (email_check, account_check))

					connection.commit()

				else:

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