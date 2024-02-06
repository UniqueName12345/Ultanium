import os
import json

# check if account.json exists and is not empty
if os.path.exists('account.json') and os.path.getsize('account.json') > 0:
    with open('account.json', 'r') as file:
        account_info = json.load(file)
    username = account_info["username"]
    password = account_info["password"]
else:
    username = input("Username: ")
    password = input("Password: ")
    account_info = {"username": username, "password": password}
    with open('account.json', 'w') as file:
        json.dump(account_info, file)

# set the environment variables
os.environ["ultusername"] = username
os.environ["ultpassword"] = password

import meower # this is the bot itself