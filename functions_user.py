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
        logging.info(f"new user created with email {email} and name {name}")
    except mysql.connector.errors.IntegrityError:
        logging.warning('User already exists')
    except:
        loging.error("Error creating new user")

def login(email, password):
    try:
        cursor.execute(f"SELECT * FROM mydb.users WHERE email='{email}' AND password='{password}';")
        id = cursor.fetchall()[0][0]
        with open('credentials.txt', 'w') as f:
            credentials = str(id) + '\n' + email + '\n' + password
            f.write(credentials)
        logging.info(f"Succesfully logged in with email {email}")
        return 0
    except IndexError:
        return 1
    except:
        return 2