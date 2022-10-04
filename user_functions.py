import logging
import connect

mydb = connect.mydb
cursor = connect.cursor

def create_user(email, name, password):
    print(email, name, password)
    try:
        cursor.execute(f"INSERT INTO users (`email`, `user name`, `password`) VALUES ('{email}', '{name}', '{password}')")
        mydb.commit()
        loging.info(f"Succesfully created user with email: {email}, user name: {name}, password: {password}")
    except mysql.connector.errors.IntegrityError:
        logging.warning('User already exists')
    except:
        loging.error('Error creating new user')