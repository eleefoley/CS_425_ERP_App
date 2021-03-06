#for handling tables of data within python
import sys
import pandas
#for connection to and communication to the posgres database
import psycopg2
from psycopg2 import Error



def main():


    try:
        un,pw,db = ask_for_connection_info()
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
        grant_user_roles(username,role,password)
        execute_role (username, role, password)

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error ", error)

    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    print("""Thanks for accessing and interacting with Database ERP for
    Illinois Tech project for CS 425, Database Organization, taught by Ola Tannous.
    This project was completed by Emma Foley and Nicholas Elson""")

def ask_for_connection_info():
    option = input("""Would you like to provide connection information for a local posgres database or use what is included in the origincal project: 
                   (a) local info
                   (b) info from the original project""")
    done = False
    while(done==False):
        if(option =='a'):
            db = input("Please type in the name of the database: ")
            un = input("Please type in the username, with correct casing: ")
            pw = input("Please type in the password, with correct casing: ")
            done = True
        elif(option =='b'):
            un = "postgres"
            pw = "B2good#1"
            db = "erp"
            done = True
    return un,pw,db



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
                        'SQL/create_engineer.sql','SQL/create_hr.sql'
                        ]
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
#             print(user_info.query('username == "' + str(un) + '"'))
            if user_info.loc[user_info['username'] == str(username), 'pw'].values == password:
                login = True
    #               print(list(user_info.query('username == "' + str(un) + '"')))
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
    query = """DO
                $do$
                BEGIN
                   IF NOT EXISTS (
                      SELECT FROM pg_catalog.pg_user  -- SELECT list can be empty for this
                      WHERE  usename = '""" + username + """') THEN
                      CREATE user """ + username + """ with in role """ + role + " LOGIN PASSWORD '" + password + """' ;
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
        admin_connect()
        create_login_table()
    except:
        print("Okay, so you're in our records, but not in the database.  We'll add you as a user with the " + role + " permissions real quick.")
        try:
            connection = admin_connect()
            cursor = connection.cursor()
            cursor.execute(query)
            print("User created")
            connection.commit()
            create_login_table()
            connection.commit()
            cursor.close()
            connection.close()

            connection = psycopg2.connect(user = username,
                                      password = password,
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "erp")
            print("Cool, we found your username in the database you have all of the " + role + " permissions.") 
 
        except (Exception, psycopg2.DatabaseError) as error :
            print (error)

    #get_userID_query = """select userID from employeeLogin where userName = '""" + username +"""';"""
    #cursor = connection.cursor()
    #cursor.execute(get_userID_query)
    #userID = cursor.fetchone()
    insert_login(username,role)

    #closing database connection.
    if(connection):
           print("PostgreSQL connection is closed")
    update_logout(username)
    return(username,role) 

def grant_user_roles(username,role,password):
    connection = admin_connect()
    cursor = connection.cursor()
    if role == 'engineer':
        query = """DO
                $do$
                BEGIN
                
                    
                    
                    grant select on engineerView to engineer;
                    grant update,select on model to engineer;
                    grant update,select on inventory to engineer;
              
                END
                $do$;"""


    if role == 'admin':
        query = """DO
        $do$
        BEGIN
            grant all privileges on database erp to admin;
            grant all privileges on all tables in schema public to admin;
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin;
            grant select on expenseReport to admin;
            grant select on customerModel to admin;
              
        END
        $do$;"""
    if role == 'hr':
                query = """DO
                $do$
                BEGIN
                
                    grant update,select on employee to hr;
                    grant select on hrView to hr;
                    grant select on orders to hr;
              
                END
                $do$;"""
    if role == 'sales':
                query = """DO
                $do$
                BEGIN
                
                    GRANT select on salview TO sales;
                    GRANT update,select ON customer to sales;
                    grant insert, select on orders to sales;
              
                END
                $do$;"""

    cursor.execute(query)
    connection.commit()

    


def create_login_table():
	connection = admin_connect()
	cursor = connection.cursor()
	query = """CREATE TABLE IF NOT EXISTS login (
			username varchar(25),
			privelege varchar (25),
			loginTime timestamp,
			logoutTime timestamp
			);
		"""
	cursor.execute(query)
	cursor.close()

def admin_connect():
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "B2good#1",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "erp")
    except (Exception, psycopg2.DatabaseError) as error :
        print(error)
    return connection       

def insert_login(username,role):
    try:
        connection = admin_connect()
        cur2 = connection.cursor() 
        login_insert = """Insert into login (username, privelege, loginTime) 
                         values ('""" + username + """','""" + role + """' ,now());"""


        cur2.execute(login_insert)
        connection.commit()
        cur2.close()
        print("Added a record of your login") 
    except (Exception, psycopg2.DatabaseError) as error :
        print(error)
    finally:
        if(connection):
            connection.close()   

def update_logout(username):
    try:
        connection = admin_connect()
        cur3 = connection.cursor()
        logout_update = """update login set logouttime = now() 
                               where logoutTime is null 
                               and username = '""" + username + """' and loginTime = (
	                       select min(loginTime) from login where logoutTime is null and username = '""" + username + """'
                               );"""

        cur3.close()
        connection.close()
        print("Added a record of your logout")
    except (Exception, psycopg2.DatabaseError) as error :
        print(error)
    finally:   
        if(connection):
            connection.close()



def prompt_for_inventory_update(connection):
    done = False
    print("Update a field in Inventory for a specific inventory number")
    while(done==False):
        response = input("""Which of the following fields would you like to update:
                         (a) Cost
                         (b) LeadTime
                         (c) CategoryType
                         (d) Amount
                         or
                         (e) Exit this prompt without updating
                         """)
        if(response=='e'):
            done = True
        elif(response=='a'):
            field = "cost"
        elif(response=='b'):
            field = "LeadTime"
        elif(response=='c'):
            field = "CategoryType"
        elif(response == 'd'):
            field = "Amount"
        new_value = input("Type the desired value: ")
        pk = input("Type the inventory ID of the item you would like to update: ")

        query = """update inventory set """ + str(field) + """ = '""" + str(new_value) + """' where inventoryid = """ + str(pk) + """;""" 
#         print(query)
        done = True
        see_result_query = "select * from inventory where inventoryid = " + str(pk) + ";"
        try:
            cursor = connection.cursor()
            connection.commit()
            cursor.execute(query)
            print("Update complete")
            connection.commit()    
            print("Commited update")
            cursor.execute(see_result_query)
            row = cursor.fetchall()
            row = pandas.DataFrame(row)
            print(row)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error ", error)

def prompt_for_model_update(connection):
    table = "model"
    primary_key = "modelnumber"
    done = False
    print("Update a field in " + table + " for a specific" + primary_key)
    while(done==False):
        response = input("""Which of the following fields would you like to update:
                         (a) salePrice
                         or
                         (b) Exit this prompt without updating
                         """)
        if(response=='b'):
            done = True
        elif(response=='a'):
            field = "salePrice"
        new_value = input("Type the desired value: ")
        pk = input("Type the " + primary_key + " of the item you would like to update: ")

        query = "update " + table +" set " + str(field) + " = '" + str(new_value) + "' where " + primary_key + " = " + str(pk) + ";" 
        print(query)
        done = True
        see_result_query = "select * from " + table + " where " + primary_key + " = " + str(pk) + ";"
        try:
            cursor = connection.cursor()
            connection.commit()
            cursor.execute(query)
            print("Update complete")
            connection.commit()    
            print("Commited update")
            cursor.execute(see_result_query)
            row = cursor.fetchall()
            row = pandas.DataFrame(row)
            print(row)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error ", error)

def prompt_for_sales_customer_view(connection):
    done = False
    print("View customer's information.")
    while(done==False):
        response = input("""How will you be searching for your customer:
                         (a) By first name
                         (b) By last name
                         (c) By customerID
                         or
                         (d) Exit this prompt without viewing
                         """)
        if(response=='d'):
            done = True
        elif(response=='a'):
            field = "upper(firstname)"
            new_value = input("Type the desired first name: ")
            new_value = "upper('" + new_value + "')"
        elif(response=='b'):
            field = "upper(lastname)"
            new_value = input("Type the desired last name: ")
            new_value = "upper('" + new_value + "')"
        elif(response=='c'):
            field = "customerid"
            new_value = input("Type the desired id: ")

        query = """select * from customer where """ + str(field) + """ = """ + str(new_value) + """;""" 
#         print(query)
        done = True
        see_result_query = """select * from customer where """ + str(field) + """ = """ + str(new_value) + """;"""
        try:
            cursor = connection.cursor()
            connection.commit()
            cursor.execute(query)
            print("View complete")
            connection.commit()    
            print("Commited update")
            cursor.execute(see_result_query)
            row = cursor.fetchall()
            row = pandas.DataFrame(row)
            print(row)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error ", error)

def prompt_for_customer_update(connection):
    done = False
    print("Update a field in customer for a specific inventory number")
    while(done==False):
        response = input("""Which of the following fields would you like to update:
                         (a) first name
                         (b) last name
                         or
                         (c) Exit this prompt without updating
                         """)
        if(response=='c'):
            done = True
        elif(response=='a'):
            field = "firstname"
        elif(response=='b'):
            field = "lastname"

        new_value = input("Type the desired name: ")
        pk = input("Type the customer ID of the person you would like to update: ")

        query = """update customer set """ + str(field) + """ = '""" + str(new_value) + """' where customerid = """ + str(pk) + """;""" 
#         print(query)
        done = True
        see_result_query = "select * from customer where customerid = " + str(pk) + ";"
        try:
            cursor = connection.cursor()
            connection.commit()
            cursor.execute(query)
            print("Update complete")
            connection.commit()    
            print("Commited update")
            cursor.execute(see_result_query)
            row = cursor.fetchall()
            row = pandas.DataFrame(row)
            print(row)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error ", error)


def prompt_for_orders_insert(connection):
    done = False
    print("Enter a new order:")
    ordernum = input("Enter an order Number: ")
    customerId = input("Enter a customer ID: ")
    empId = input("Enter an employee's ID: ")
    modNum = input("Enter a model number: ")
    sale = input("Enter a sale value: ")

    query = "insert into orders (ordernumber, customerid, employeeid, modelnumber, salevalue) VALUES ('"+ str(ordernum) + "','"+str(customerId)+"','"+str(empId)+"','"+str(modNum)+"','"+str(sale)+"');" 
#         print(query)
    done = True
    see_result_query = "select * from orders where ordernumber = " + str(ordernum) + ";"
    try:
        cursor = connection.cursor()
        connection.commit()
        cursor.execute(query)
        print("Update complete")
        connection.commit()    
        print("Commited update")
        cursor.execute(see_result_query)
        row = cursor.fetchall()
        row = pandas.DataFrame(row)
        print(row)
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error ", error)


def prompt_for_hr_orderhistory_view(connection):
    done = False
    print("View order's information.")
    while(done==False):
        response = input("""How will you be searching for your order:
                         (a) Order Number
                         (b) Customer ID
                         (c) Employee ID
                         (d) Model Number
                         (e) Sale value
                         or
                         (f) Exit this prompt without viewing
                         """)
        if(response=='f'):
            done = True
        elif(response=='a'):
            field = "ordernumber"
            new_value = input("Type the desired ordernumber: ")
        elif(response=='b'):
            field = "customerid"
            new_value = input("Type the desired customerid: ")
        elif(response=='c'):
            field = "employeeid"
            new_value = input("Type the desired employee id: ")
        elif(response=='d'):
            field = "modelnumber"
            new_value = input("Type the desired modelnumber: ")
        elif(response=='e'):
            field = "salevalue"
            new_value = input("Type the desired sale value: ")

        query = """select * from orders where """ + str(field) + """ = """ + str(new_value) + """;""" 
#         print(query)
        done = True
        see_result_query = """select * from orders where """ + str(field) + """ = """ + str(new_value) + """;"""
        try:
            cursor = connection.cursor()
            connection.commit()
            cursor.execute(query)
            print("View complete")
            connection.commit()    
            print("Commited update")
            cursor.execute(see_result_query)
            row = cursor.fetchall()
            row = pandas.DataFrame(row)
            print(row)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error ", error)

def prompt_for_employee_update(connection):
    table = "employee"
    primary_key = "employeeid"
    done = False
    print("Update a field in " + table + " for a specific" + primary_key)
    while(done==False):
            response = input("""Which of the following fields would you like to update:
                             (a) firstName
                             (b) middleName
                             (c) lastName
                             (d) salary (numbers only, no commas or dollar signs)
                             (e) salaried (true/false)
                             (f) hourly (true/false)
                             (g) department
                             or
                             (h) Exit this prompt without updating
                             """)
            if(response=='h'):
                done = True
            elif(response=='a'):
                field = "firstName"
            elif(response=='b'):
                field = "middleName"
            elif(response=='c'):
                field = "lastName"
            elif(response == 'd'):
                field = "salary"
            elif(response=='e'):
                field = "salaried"
            elif(response=='f'):
                field = "hourly"
            elif(response == 'g'):
                field = "department"
            new_value = input("Type the desired value: ")
            pk = input("Type the " + primary_key + " of the item you would like to update: ")

            query = "update " + table +" set " + str(field) + " = '" + str(new_value) + "' where " + primary_key + " = " + str(pk) + ";" 
            print(query)
            done = True
            see_result_query = "select * from " + table + " where " + primary_key + " = " + str(pk) + ";"
            try:
                cursor = connection.cursor()
                connection.commit()
                cursor.execute(query)
                print("Update complete")
                connection.commit()    
                print("Commited update")
                cursor.execute(see_result_query)
                row = cursor.fetchall()
                row = pandas.DataFrame(row)
                print(row)
                cursor.close()
            except (Exception, psycopg2.DatabaseError) as error :
                print ("Error ", error)









def execute_role (username, role, password):
    i = 'y'
    connection = psycopg2.connect(user = username,
                                    password = password,
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "erp")

    cursor = connection.cursor()
# Engineer's prompt
    if role == 'engineer':
        print('''As an ''' + role + ''', you have permission to see employees,
        and change model or inventory infromation.''')
        while i == 'y':
            option = input('''Please enter: \n 
            (a) to view employees \n 
            (b) to update model information through prompts \n 
            (c) to update inventory information through prompts \n
            (d) to quit \n''')
#           engineerView
            query = '-1'
            if option == 'a':
                query = 'select * from engineerView'

            elif option == 'b':
#           update model information                    
                prompt_for_model_update(connection)
                i = 'y'

#           update through prompt
            elif option == 'c':
                prompt_for_inventory_update(connection)
                i = 'y'
            elif option == 'd':
                i = -1
            else:
                print('Invalid selection.')
            if query != '-1':
#   Run query
                try: 
                    cursor.execute(str(query))
                    ex = cursor.fetchall()
                    ex = pandas.DataFrame(ex)
                    print(ex)
                except(Exception, psycopg2.DatabaseError) as error :
                    print('Error: ' +error+ ',...')
                i= input('Would you like to run another query? \n(Enter (y) to continue): \n')
            
# Admin's prompt
    elif role == 'admin':
        print ('''As an ''' + role + ''' you have permission to all priveleges on this database, 
        as well as access to four different analytic reports.''')
        while i == 'y':
            query = '-1'
            option = input('''Please enter: \n
            (a) to enter a SQL query \n
            (b) to access admin report #1: Total revenue from sales, associated employee and customer \n
            (c) to access admin report #2: Customer model bought and quantity to make prediction and understand trending \n
            (d) to access admin report #3: For each order, the associated parts and available inventory\n
            (e) to access admint report #4: Expense report, employee showing salary, bonus expense and part cost \n
            (f) to exit \n''')

        #   Any SQL query
            if option == 'a':
                query = input('Please enter your SQL query: \n')
                try: 
                    cursor.execute(str(query))
                    connection.commit()
                    ex = cursor.fetchall()
                    ex = pandas.DataFrame(ex)
                    print(ex)
                except(Exception, psycopg2.DatabaseError) as error :
                    print('Error: ' + str(error) + ',...')
                query = '-1'
                

            # admin report #1
            elif option == 'b':
                admin_r = 'SQL/admin_one.sql'
                query = open(admin_r).read()

        #     admin report #2
            elif option == 'c':
                admin_r = 'SQL/admin_two.sql'
                query = open(admin_r).read()


        #     admin report #3
            elif option =='d':
                admin_r = 'SQL/admin_three.sql'
                query = open(admin_r).read()


        #      admin report #1
            elif option =='e':
                admin_r = 'SQL/admin_four.sql'
                query = open(admin_r).read()

        #        exit
            elif option =='f':
                i= -1

            else:
                print('Invalid selection.')

            if query != '-1':
#   Run query
                try: 
                    cursor.execute(str(query))
                    ex = cursor.fetchall()
                    ex = pandas.DataFrame(ex)
                    print(ex)
                except(Exception, psycopg2.DatabaseError) as error :
                    print('Error: ' +error+ ',...')
                i= input('Would you like to run another query? \n(Enter (y) to continue): \n')

# Hr prompt
    elif role == 'hr':
        print ('''As an ''' +role+ ''' you have permissions to update employee records,
        and view which employ sold any order.''')
        while i == 'y':
            query = '-1'
            option = input('''Please enter: \n
            (a) to update an employee's information \n
            (b) to view order history for all employees \n
            (c) to view oder history for a particular employee or order \n
            (d) to exit \n''')

        #       update employee
            if option == 'a':
                prompt_for_employee_update(connection)
                i = 'y'

        #     hrview - all
            elif option == 'b':
                query = 'select * from hrView'


        #      hrview - specific
            elif option == 'c':
                prompt_for_hr_orderhistory_view(connection)
                i='y'

        #     exit
            elif option == 'd':
                i= -1

            else:
                print('Invalid selection')

            if query != '-1':
#   Run query
                try: 
                    cursor.execute(str(query))
                    ex = cursor.fetchall()
                    ex = pandas.DataFrame(ex)
                    print(ex)
                except(Exception, psycopg2.DatabaseError) as error :
                    print('Error: ' +error+ ',...')
                i= input('Would you like to run another query? \n(Enter (y) to continue): \n')


# Sales prompt
    elif role == 'sales':
        print('''As ''' +role+ ''' you have permission to view customer information,
        update customer information, and insert new orders.''')
        while i == 'y':
            query = '-1'
            option = input('''Please enter: \n
            (a) to view all customer information \n
            (b) to view a specific customer's information \n
            (c) to update customer information \n
            (d) to insert a row into orders \n
            (e) to exit \n''')

        #     salview - all
            if option == 'a':
                query = 'select * from salview'


        #    salview - specific
            elif option == 'b':
                prompt_for_sales_customer_view(connection)
                i = 'y'


        #     update customer
            elif option == 'c':
                prompt_for_customer_update(connection)
                i = 'y'


        #     insert into orders
            elif option == 'd':
                prompt_for_orders_insert(connection)
                i = 'y'


        #    exit
            elif option == 'e':
                i = -1

            else:
                print ('Invalid selection.')

            if query != '-1':
#   Run query
                try: 
                    cursor.execute(str(query))
                    ex = cursor.fetchall()
                    ex = pandas.DataFrame(ex)
                    print(ex)
                except(Exception, psycopg2.DatabaseError) as error :
                    print('Error: ' +error+ ',...')
                i= input('Would you like to run another query? \n(Enter (y) to continue): \n')



    else:
        print('Your role, ' + role + ', does not have any priveleges.')




main()



