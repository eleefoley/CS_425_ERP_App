import sys
import pandas as pd

def login_user():
	user_info = pd.read_csv("Data/unpwd.csv")

	login = False
	while login == False:
		un = input("Enter your username: ")
		print(un)
		if un in list(user_info['userID']): 
			pw = input("Enter your password: ")
			if user_info.query('userID == "' + str(un) + '"')['pw'][0] == pw:
				login = True
		else:
			print("User name not found.  Try again.")

login_user()

