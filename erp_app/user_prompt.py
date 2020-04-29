import sys
import pandas
import psycopg2

def login_user():
    user_info = pandas.read_csv("../erp_app/Data/unpwd.csv")

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


            
[results] = login_user()
username = results[0]
role = results[1]
password = results[2]

login_db_user(username,role,password)
