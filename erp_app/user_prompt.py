import sys
import pandas
import psycopg2

def login_user():
    user_info = pandas.read_csv("../erp_app/Data/unpwd.csv")

    login = False
    i = 0
    while login == False or i >= 3:
        username = input("Enter your username: ")
        print(username)
        if username in list(user_info['userID']):
            password = input("Enter your password: ")
            print(password)
#             print(user_info.query('userID == "' + str(un) + '"'))
            if user_info.loc[user_info['userID'] == str(username), 'pw'].values == password:
                login = True
    #               print(list(user_info.query('userID == "' + str(un) + '"')))
            else:
                print('Incorrect. ')
                i = i +1
        else:
            print("User name not found.  Try again.")
            i = i +1
    return user_info.loc[user_info['userID'] == str(username)].values.tolist()

def check_db_user(username,role,password):
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
        cursor = connection.cursor()
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
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


[results] = login_user()
username = results[0]
role = results[1]
password = results[2]

check_db_user(username,role,password)
