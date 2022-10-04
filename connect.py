import mysql.connector 
import MySQLdb
import logging

with open('dbconnection.txt', 'r') as f:
    host = f.readline()
    user = f.readline()
    passwd = f.readline()

mydb = mysql.connector.connect(host = host, user = user, passwd = passwd, database = 'mydb')
cursor = mydb.cursor()
print(mydb)