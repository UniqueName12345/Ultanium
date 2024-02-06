import os

username = input("Username: ")
password = input("Password: ")

# set the environment variables
os.environ["USERNAME"] = username
os.environ["PASSWORD"] = password

import meower # this is the bot itself