import mysql.connector 
import logging
import pickle

with open('dbconnection.bin', 'rb') as f:
    credentials = pickle.load(f)
    host, user, password, version = credentials

try:
    mydb = mysql.connector.connect(host = host, user = user, password = password, database = 'mydb')
    cursor = mydb.cursor(buffered=True)
    print(mydb)
except:
    print("Connection lost")