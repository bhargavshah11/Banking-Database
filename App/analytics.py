import pymysql
import pymysql.cursors
import json
import re

# -------- Connection to the Database ------------------------------------------------

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='pwd',  # Enter your sql db password here
                             db='banking',  # Enter your db name here
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

    except ValueError:
        raise ValueError("Account number entered is invalid")


# -------------------------------- Validating Email ID ------------------------------

def validate_email(json_data):

    # Assuming this is received from bank.
    email_id_update = json_data["account_information"]["email_address"]
    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_id_update) is not None:
        return True

    raise ValueError("Email address entered is Invalid")


# -------- Updating Email ID in the Database ----------------------------------

def update_email(json_data, cnx):

    account_id_check = json_data["account_id"]
    email_id_update = json_data["account_information"]["email_address"]

    try:

        # Update email address in database
        sql = "UPDATE clients SET email_address = %s WHERE account_id = %s"
        cnx.execute(sql, (email_id_update, account_id_check))
        connection.commit()

        sql = "SELECT concat(first_name,' ', last_name) FROM update_info"
        cnx.execute(sql)
        client_name = cnx.fetchone()
        print("Hi " + client_name[0] + "!")

        sql = "SELECT email_address FROM update_info"
        cnx.execute(sql)
        clients_email = cnx.fetchone()

        print("\n" + "Your email ID has been updated to: " + clients_email[0])

    except ValueError:
        return False


# -------- Updating Address in the Database -------------------------------------

def update_address(json_data, cnx):

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

        cnx.execute(sql, (street_num_update, street_name_update, unit_num_update, city_update, state_update, zip_update,
                          account_id_check))
        connection.commit()

        # Response
        sql = "SELECT concat(street_number,' ',street_name,' ',unit_number,' ',city,' ',state,' ',zip_code) FROM " \
              "update_info "
        cnx.execute(sql)
        clients_address = cnx.fetchone()
        print("\n" + "Address:", clients_address[0])

    except TypeError:
        raise TypeError("Address entered is invalid or has empty fields")


# -------- Main function that executes only if account ID is validated ----------------

def update(filename):

    with open(filename) as json_file:
        json_data = json.load(json_file)

    account_id_check = json_data["account_id"]

    try:
        with connection.cursor() as cnx:
            rows = validate_account(json_data, cnx)

            # Execute the validate methods only if account_ID is found in the database
            if rows is not None:

                if validate_email(json_data):
                    update_email(json_data, cnx)
                    update_address(json_data, cnx)

                    sql = "SELECT * FROM clients WHERE account_id = %s"
                    cnx.execute(sql, account_id_check)
                    row = cnx.fetchone()

                    while row is not None:
                        print("\n" + "Here is the updated account information:" + "\n", row)
                        row = cnx.fetchone()

                    cnx.close()

    finally:
        connection.close()


if __name__ == '__main__':
    update("record.json")
