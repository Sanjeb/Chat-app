import mysql.connector 
import MySQLdb

mydb = mysql.connector.connect(host = '129.154.40.30', user = 'app', passwd = 'password', database = 'mydb')
cursor = mydb.cursor()
print(mydb)

def create_user(email, name, password):
    print(email, name, password)
    try:
        cursor.execute(f"INSERT INTO users (`email`, `user name`, `password`) VALUES ('{email}', '{name}', '{password}')")
        mydb.commit()
    except mysql.connector.errors.IntegrityError:
        print("User already exists")
    except:
        print('unknown error')

create_user('sanjeev.selvam@gmail.com', 'sanjeev', 'sanjeev')