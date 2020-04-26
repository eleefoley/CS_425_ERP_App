import sys
import pandas
import psycopg2

def login_user():
    user_info = pandas.read_csv("../erp_app/Data/unpwd.csv")

    login = False
    while login == False:
        un = input("Enter your username: ")
        print(un)
        if un in list(user_info['userID']):
            pw = input("Enter your password: ")
            print(pw)
#             print(user_info.query('userID == "' + str(un) + '"'))
            if user_info.loc[user_info['userID'] == str(un), 'pw'].values == pw:
                login = True
    #               print(list(user_info.query('userID == "' + str(un) + '"')))
            else:
                print('Incorrect. ')
        else:
            print("User name not found.  Try again.")
    return user_info.loc[user_info['userID'] == str(un)].values.tolist()

def check_db_user(username,role,password):
    query = '''DO
                $do$
                BEGIN
                   IF NOT EXISTS (
                      SELECT FROM pg_catalog.pg_user  -- SELECT list can be empty for this
                      WHERE  usename = "''' + username + '''") THEN

                      CREATE user "''' + username + '''" with ''' + role + ''' LOGIN PASSWORD "''' + password + '''" ;
                   END IF;
                END
                $do$;'''

    try:
        connection = psycopg2.connect(user = username,
                                      password = password,
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "erp")
        print("Cool, we found your username in the database you have all of the " + role + "permissions")
        cursor = connection.cursor()
    except:
        print("Okay, so you're in our records, but not in the database.  We'll add you as a user with the " + role + " permissions real quick.")
        try:
            connection = psycopg2.connect(user = "postgres",
                                      password = "cs425proj",
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
