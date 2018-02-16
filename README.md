# Banking-Database
Updating Client information using Relational Database Management System. 

## Scenario
A client (e.g. a bank) sends data whenever their customers modify their account information. For example, they may tell us when a customer changes their email address on file. The client sends this data as JSON records to a REST API endpoint, example of which are below.

**Assume the account ID field is unique.**

```
{
'account_id': 1121345,
'account_information': {
'address': {
'city': 'Centerville',
'state': 'CA',
'street_name': 'Main Street',
'street_number': '123',
'zip_code': '91111'},
'date_of_birth': '1986-08-18',
'email_address': 'john_doe@gmail.com',
'first_name': 'John',
'last_name': 'Doe'},
'account_standing': 'G',
'event_date': '2017-08-24'}
```

Write code to process these records to create a view with the most up-to-date information on each account. That is, we would like to query the most recent PII based on the account ID.


## Setup

**1.MySQL** [Installation Documentation](https://dev.mysql.com/doc/refman/5.6/en/osx-installation-pkg.html)
 - Install MySQL on your system (Mac/Windows etc) 
 - Create an account 
 - Turn the MySQL server **ON**
 - Go to Terminal 
 - Follow the steps given in Banking-Database/Database/database.sql

**2.PyMySQL** [Installation Documentation](https://pypi.python.org/pypi/PyMySQL)
- The goal of PyMySQL is to be a drop-in replacement for MySQLdb
  - To create [Database connection](https://pypi.python.org/pypi/PyMySQL#documentation). 

**3.Python 3** [Download Here](https://www.python.org/downloads/)

## Importing Modules

$ pip install PyMySQL  
$ pip install unittest

```
import pymysql
import pymysql.cursors
import json
import re
```

## Running UnitTests

There are 3 individual unittests in the **UnitTest** folder. All files are customized according to input **JSON RECORD**. Each test checks for different issues as follows:

Python Command to RUN UNIT TEST:

```python -m unittest -v test_module.py```

**Test 1**
- Checks for Invalid Email Id entered in the json record

**Test 2**
- Checks for errors in the address entered in the json record

**Test 3**
- Checks for Account ID entered in the json record 

**More tests considered:**
1. Cross validating Birth-date with Account ID
2. Cross validating First-Last Name with the Account ID
3. Cross validating Birth- date and First-Last Name with the Account ID
4. Check for Integers instead of string and vice-versa.

## FAQs

**1. How does your solution handle malformed or corrupt data?**
- Step 1: Verifying the Account ID with the existing database. If account ID not validated, discard the input and raise error.
- Step 2: If Account ID is verified. We check for Email ID validation that the user requested to update. If Email ID fails the validation test. Discard the input and raise error. 
- Step 3: Check for Address update. If street number is in alphabets (For e.g. "sdfy"), discard any update request and raise error.

**2. Is your solution optimized for query latency or throughput?**
- Query Latency

**3. What would you do differently if the client doesn’t send the account ID?**
- Assuming **Account ID** field is unique from the information that the client sends; we consider it to be a deciding data point to further process anything. If client doesn't send or provides an invalid (Not in the exisiting DB) *account id* then we discard the input record and raise an error that reads "Account number entered is Invalid" after cross validating it with the exisitng database.  

**4. If the view gets very large (can no longer fit into memory), how can we modify it to ensure we’re still able to look up examples?**
- First questions that pops-up is that "What is counted as very large?"
  - Assuming it could either be a couple thousand, a million, couple million entries or more.
  - **Option 1:** Pagination that shows a few rows at a time in specific range (. 
  - **Option 2:** A filter that can sort information in *alphabatical order (Name), Most recently updated,* etc.
  - **Option 3:** Filter out using SQL queries to only search using *Account ID*. Since it's unique, only one result will pop-up instead of those thousands or millions of records. (Implemented in this project) 
  - **Option 4:** Only show records that were updated in the last one month/year. 
  
  
## Assumptions

1. Two users can have the same address.
2. Account ID is unqiue.
3. Every user has an email address
4. User has nothing to do with "Account_standing"
5. Birth-date, First Name, and Last Name stays the same. 
6. Address update request can be sent.
7. View can be changed as per needs. 
