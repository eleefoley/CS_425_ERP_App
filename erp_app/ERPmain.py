#for handling tables of data within python
import sys
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

def main():

    try:
        connection = psycopg2.connect(user = un,
                                      password = pw,
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = db)

        cursor = connection.cursor()
        print ('Connection to PostgreSQL secure')
 
        create_tables(cursor, connection)
        create_roles(cursor, connection)
        fill_tables (cursor, connection)



        [results] = login_user()
        username = results[0]
        role = results[1]
        password = results[2]

        login_db_user(username,role,password)
 

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error ", error)

    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")







# table_has_data(table_name,cursor) checks if PostgreSQL tables have any rows
def table_has_data(table_name, cursor):
    check_query = ("SELECT EXISTS(SELECT * FROM {table_name})".format(
		table_name = table_name))
    cursor.execute(check_query)
    return cursor.fetchone()[0]

# create_tables(cursor,connection) creates any tables that do not already exist in PostgreSQL
def create_tables(cursor, connection):
    required_tables = ['SQL/create_inventory.sql','SQL/create_model.sql',
                           'SQL/create_employee.sql','SQL/create_customer.sql',
                           'SQL/create_orders.sql','SQL/create_employeeLogin.sql',
                           'SQL/create_login.sql']
    for sql_file in required_tables:
        query = open(sql_file).read()
        cursor.execute(query)
        connection.commit()
    print('All of the tables are present in PostgreSQL Database.')

# create_roles(cursor,connection) creates any roles that do not already exist in PostgreSQL
def create_roles(cursor, connection):
    required_roles = ['SQL/create_sales.sql','SQL/create_admin.sql',
                        'SQL/create_engineer.sql','SQL/create_hr.sql']
    for sql_roles in required_roles:
        query = open(sql_roles).read()
        cursor.execute(query)
        connection.commit()
    print("All necessary roles exist in PostgreSQL.")

# fill_tables(cursor,connection) fills any tables with data from csv files)
def fill_tables(cursor, connection):
    i = 0
    table_names = ['Inventory', 'Model','Employee','Customer','Orders','EmployeeLogin']
    filled_tables = ['Data/inventory.csv','Data/model.csv',
                    'Data/employee.csv','Data/customer.csv',
                    'Data/order.csv', 'Data/employeeLogin.csv']
    while i <= 5:
        tab = table_names[i]
        fill = filled_tables[i]
        # if table has any rows, increment without copying any data
        if table_has_data(tab, cursor):
            i = i +1
        else:
            file = open(fill, 'r')
            cursor.copy_from(file, tab, sep=',')
            file.close()
            connection.commit()
            i = i + 1
    print ('CSV files of data have been copied into PostgreSQL tables.')


def login_user():
    user_info = pandas.read_csv("Data/unpwd.csv")

    login = False
    i = 0
    while login == False and i <= 3:
        username = input("Enter your username: ")
        print(username)
        if username in list(user_info['username']):
            password = input("Enter your password: ")
            print(password)
            print(user_info.query('username == "' + str(un) + '"'))
            if user_info.loc[user_info['username'] == str(username), 'pw'].values == password:
                login = True
                print(list(user_info.query('username == "' + str(un) + '"')))
            else:
                print('Incorrect. ')
                i = i +1
        else:
            print("User name not found.  Try again.")
            i = i +1
    if login == False:
        print("Too many incorrect tries")
        exit()
    return user_info.loc[user_info['username'] == str(username)].values.tolist()

def login_db_user(username,role,password):
    print("Let's try logging you into the database")
    query = """DO
                $do$
                BEGIN
                   IF NOT EXISTS (
                      SELECT FROM pg_catalog.pg_user  -- SELECT list can be empty for this
                      WHERE  usename = '""" + username + """') THEN
                      CREATE user """ + username + """ with role """ + role + " LOGIN PASSWORD '" + password + """' ;
                   END IF;
                END
                $do$;"""

    try:
        connection = psycopg2.connect(user = username,
                                      password = password,
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "erp")
        print("Cool, we found your username in the database you have all of the " + role + " permissions.")
        #create_login_table(connection)
    except:
        print("Okay, so you're in our records, but not in the database.  We'll add you as a user with the " + role + " permissions real quick.")
        try:
            connection = psycopg2.connect(user = "postgres",
                                      password = "B2good#1",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "erp")
            cursor = connection.cursor()
            cursor.execute(query)
            print("User created")
            connection.commit()
            create_login_table(connection)
            connection.commit()
            cursor.close()
            connection.closer()

            connection = psycopg2.connect(user = username,
                                      password = password,
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "erp")
            print("Cool, we found your username in the database you have all of the " + role + " permissions.") 
 
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)

    get_userID_query = """select userID from employeeLogin where userName = '""" + username +"""';"""
    cursor = connection.cursor()
    cursor.execute(get_userID_query)
    userID = cursor.fetchone()
    cur2 = connection.cursor()
    login_insert = """Insert into login (userID, username, loginTime) 
                         values (""" + str(userID) + """,'""" + username + """',now());"""

    cur2.execute(login_insert)
    connection.commit()
    cur2.close()

    #closing database connection.
    if(connection):
            cur3 = connection.cursor()
            logout_update = """update login set logouttime = now() 
                               where logoutTime is null 
                               and username = '""" + username + """' and loginTime = (
	                       select min(loginTime) from login where logoutTime is null and username = '""" + username + """'
                               );"""

            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def create_login_table(connection):
	cursor = connection.cursor()
	query = """CREATE TABLE IF NOT EXISTS login (
			userID int,
			username varchar(25)
			privelege varchar (25),
			loginTime timestamp,
			logoutTime timestamp
			);
		--create a sequence for the primary key of the table so we don't have to manually assign the ID and we make sure we'll create them in order
		CREATE SEQUENCE IF NOT EXISTS userID START 1000001;
		create index IF NOT EXISTS userID_index on login(userID);"""
	cursor.execute(query)
	cursor.close()


def execute_role (username, role, password):
    i = 'y'
    try:
        connection = psycopg2.connect(user = username,
                                      password = password,
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "erp")

        cursor = connection.cursor()

        if role == 'engineer':
            print('''As an ''' + role + ''', you have permission to see employees,
        and change model or inventory infromation.''')
            while i == 'y':
                option = input('''Please enter: \n 
                (a) to view employees \n 
                (b) to update model information \n 
                (c) to update inventory information \n
                (d) to exit''')

                if option == 'a':
                    query = input('Please enter your view of employees query in SQL')
                    cursor.execute(query)
                    connection.commit()
                    i = input ('Would you like to run another query? \n(Enter (y) to continue): ')
                elif option == 'b':
                    query = input('Please enter your update of model information in SQL')
                    i= input('Would you like to run another query? \n(Enter (y) to continue):')

                elif option == 'c':
                    query = input('Please enter your update of model information in SQL')
                    i= input('Would you like to run another query? \n(Enter (y) to continue):')
                elif option == 'd':
                    i = -1
                else:
                    print('Invalid selection.')

        elif role == 'admin':
            print ('''As an ''' + role + ''' you have permission to all priveleges on this database, 
            as well as access to four different analytic reports.''')
            while i == 'y':
                option = input('''Please enter: \n
                (a) to enter a SQL query \n
                (b) to access admin report #1 \n
                (c) to access admin report #2 \n
                (d) to access admin report #3 \n
                (e) to access admint report #4 \n
                (f) to exit ''')
                if option == 'a':
                    query = input('Enter a query in postgreSQL: ')
                    cursor.execute(query)

                    i = input ('Would you like to run another query? \n(Enter (y) to continue): ')
                elif option == 'b':
                    query = """-- •	Total revenue from sales, associated employee and customer
                                select sum(orders.salevalue) as total_revenue,
                                employee.FirstName as emp_fname, 
                                employee.LastName as emp_lname, 
                                customer.FirstName as cust_fname, 
                                customer.LastName as cust_lname 
                                from orders 
                                left join employee
	                                on orders.employeeId = employee.employeeId 
                                left join customer 
	                                on orders.customerId = customer.customerId
                                group by
                                employee.FirstName, 
                                employee.LastName, 
                                customer.FirstName, 
                                customer.LastName; """
                    cursor.execute(query)


                    i = input ('Would you like to run another query? \n(Enter (y) to continue): ')
                elif option == 'c':
                    #admin report 2

                    i = input ('Would you like to run another query? \n(Enter (y) to continue): ')
                elif option =='d':
                    query = """select 
                        orders.ordernumber as order_no,
                        model.modelNumber as model_no,
                        inventory.amount as avail_inv
                        from orders
                        left join model
	                        on orders.modelnumber = model.modelnumber
                        left join inventory 
	                        on model.inventoryid = inventory.inventoryid;"""
                    cursor.execute(query)


                    i = input ('Would you like to run another query? \n(Enter (y) to continue): ')
                elif option =='e':
                    #admin report 4

                    i = input ('Would you like to run another query? \n(Enter (y) to continue): ')
                elif option =='f':
                    i= -1
                else:
                    print('Invalid selection.')


        elif role == 'hr':
            print('hello')

        elif role == 'sales':
            print('hello')
        else:
            print('Your role, ' + role + ', does not have any priveleges.')

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error ", error)

main()



