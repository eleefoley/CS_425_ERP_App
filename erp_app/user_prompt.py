import sys
import pandas as pd

def login_user():
	user_info = pd.read_csv("Data/unpwd.csv")
	login = False
	i = 0
	while login == False and i <=3:
		un = input("Enter your username: ")
		print(un)
		if un in list(user_info['userID']): 
			pw = input("Enter your password: ")
			if user_info.query('userID == "' + str(un) + '"')['pw'][0] == pw:
				login = True
			else:
				print("Incorect password. ")
				
		else:
			print("User name not found.  Try again.")
		i = i + 1
login_user()

