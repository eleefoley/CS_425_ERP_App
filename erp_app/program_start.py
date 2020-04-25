#for handling tables of data within python
import pandas

#for connection to and communication to the posgres database
import psycopg2
from psycopg2 import Error

#for making data visualizations for the reports
import plotnine

#my-local connection info
un = "postgres"
pw = "pw"
db = "erp"

def main():

    try:
        connection = psycopg2.connect(user = un,
                                      password = pw,
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = db)

        cursor = connection.cursor()

        required_tables = ['SQL/create_inventory.sql','SQL/create_model.sql',
                           'SQL/create_employee.sql','SQL/create_customer.sql',
                           'SQL/create_orders.sql','SQL/create_employeeLogin.sql',
                           'SQL/create_login.sql']

        for sql_file in required_tables:
            print('about to try ', str(sql_file))
            query = open(sql_file).read()
            cursor.execute(query)
            connection.commit()
        print("All necessary tables exists in PostgreSQL")

        required_roles = ['SQL/create_sales.sql','SQL/create_admin.sql','SQL.create_engineer.sql','SQL/create_hr.sql']

        for sql_roles in required_roles:
            query = open(sql_roles).read()
            cursor.execute(query)
            connection.commit()
        print("All necessary roles exist in PostgreSQL")


    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating PostgreSQL table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
main()
