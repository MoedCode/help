# Install Mysql on your computer
# https://dev.mysql.com/downloads/installer/

# pip install mysql-connector
# pip install mysql-connector-python

import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'help_dev',
    password = 'dev@ROOT_|25|',
    database = 'help_dev_db'
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE elderco")

print("All Done!")