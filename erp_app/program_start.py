#for handling tables of data within python
import pandas

#for connection to and communication to the posgres database
import psycopg2
from psycopg2 import Error

#for making data visualizations for the reports
import plotnine

#my-local connection info
un = "postgres"
pw = "B2good#1"
db = "erp"



connection = psycopg2.connect(user = un,
                                    password = pw,
                                    host = "127.0.0.1",
                                    port = "5432",
                                database = db)
cursor = connection.cursor()
print("Connection Secured.")

required_tables = ['SQL/create_inventory.sql','SQL/create_model.sql',
                    'SQL/create_employee.sql','SQL/create_customer.sql',
                    'SQL/create_orders.sql','SQL/create_employeeLogin.sql',
                    'SQL/create_login.sql']

for sql_file in required_tables:

    query = open(sql_file).read()
    try :
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating tables", error)
    connection.commit()
print("All necessary tables exists in PostgreSQL")

required_roles = ['SQL/create_sales.sql','SQL/create_admin.sql','SQL.create_engineer.sql','SQL/create_hr.sql']
for sql_roles in required_roles:
    query = open(sql_roles).read()
    try:
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating roles")
    connection.commit()
print("All necessary roles exist in PostgreSQL")


#closing database connection.
if(connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
