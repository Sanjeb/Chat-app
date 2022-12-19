import mysql.connector 
import logging
import pickle

with open('dbconnection.bin', 'rb') as f:
    credentials = pickle.load(f)
    host, user, password, version = credentials
    #tup = ('129.154.40.30', 'app', 'CSproj@123', 3)
    #pickle.dump(tup, f)

try:
    mydb = mysql.connector.connect(host = host, user = user, password = password, database = 'mydb')
    cursor = mydb.cursor(buffered=True)
except:
    ...