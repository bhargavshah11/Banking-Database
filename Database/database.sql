
# All the SQL queries to get you going with the database management

# Step - 1
# -------------------------- Creating the database ---------------------------

CREATE DATABASE banking;


# Step - 2
# -------------------------- Creating the table ------------------------------
# ------ Change the values of varchar, int, date as and when needed ----------

CREATE TABLE clients VALUES(account_id int, 
							event_date data, 
							account_standing varchar(10), 
							first_name varchar(10), 
							last_name varchar(10),
							date_of_birth date,
							street_number int,
							street_name varchar(10),
							unit_number varchar(10),
							city varchar(20),
							state varchar(10),
							zip_code int,
							email_address varchar(30));


# Step - 3
# ------------------------ Insert values in Database --------------------------	
# -------- You can always add more values using this same query ---------------	

INSERT INTO clients VALUES (1454581,'2018-01-09','B','Jane','Smith','1975-09-09',345,'Oak Drive','12A','Mount Pleasant','CA',90010,'hello@yahoo.com')
INSERT INTO clients VALUES (1454582,'2018-01-09','B','Mike','Jones','1975-09-09',345,'Oak Drive','12A','Mount Pleasant','CA',90010,'mike_jones@yahoo.com')
INSERT INTO clients VALUES (1454583,'2018-01-09','B','Nicola','Tesla','1975-09-09',345,'Oak Drive','12A','Mount Pleasant','CA',90010,'nicola_tesla@yahoo.com')




# After Step - 2
# ---------------- Database Description ---------------------------------------

DESCRIBE clients; 


+------------------+-------------+------+-----+---------+-------+
| Field            | Type        | Null | Key | Default | Extra |
+------------------+-------------+------+-----+---------+-------+
| account_id       | int(11)     | YES  |     | NULL    |       |
| event_date       | date        | YES  |     | NULL    |       |
| account_standing | varchar(10) | YES  |     | NULL    |       |
| first_name       | varchar(10) | YES  |     | NULL    |       |
| last_name        | varchar(10) | YES  |     | NULL    |       |
| date_of_birth    | date        | YES  |     | NULL    |       |
| street_number    | int(11)     | YES  |     | NULL    |       |
| street_name      | varchar(10) | YES  |     | NULL    |       |
| unit_number      | varchar(10) | YES  |     | NULL    |       |
| city             | varchar(20) | YES  |     | NULL    |       |
| state            | varchar(10) | YES  |     | NULL    |       |
| zip_code         | int(11)     | YES  |     | NULL    |       |
| email_address    | varchar(30) | YES  |     | NULL    |       |
+------------------+-------------+------+-----+---------+-------+



# After step - 3
# --------------- Database after inserting values in it ------------------------

SELECT * FROM clients; 

+------------+------------+------------------+------------+-----------+---------------+---------------+-------------+-------------+----------------+-------+----------+------------------------+
| account_id | event_date | account_standing | first_name | last_name | date_of_birth | street_number | street_name | unit_number | city           | state | zip_code | email_address          |
+------------+------------+------------------+------------+-----------+---------------+---------------+-------------+-------------+----------------+-------+----------+------------------------+
|    1454581 | 2018-01-09 | B                | Jane       | Smith     | 1975-09-09    |           345 | Oak Drive   | 12A         | Mount Pleasant | CA    |    90010 | hello@yahoo.com        |
|    1454582 | 2018-01-09 | B                | Mike       | Jones     | 1975-09-09    |           345 | Oak Drive   | 12A         | Mount Pleasant | CA    |    90010 | mike_jones@yahoo.com   |
|    1454583 | 2018-01-09 | B                | Nicola     | Tesla     | 1975-09-09    |           345 | Oak Drive   | 12A         | Mount Pleasant | CA    |    90010 | nicola_tesla@yahoo.com |
+------------+------------+------------------+------------+-----------+---------------+---------------+-------------+-------------+----------------+-------+----------+------------------------+




