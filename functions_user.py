import logging
import connect
import mysql.connector

mydb = connect.mydb
cursor = connect.cursor

def create_user(email, name, password, picture):
    
    command = "INSERT INTO users (`email`, `user name`, `password`, `picture`) VALUES (%s, %s, %s, %s)"
    values = (email, name, password, picture)
    print(command, values)
    cursor.execute(command, values)
    userID = cursor.lastrowid
    print(userID)
    cursor.execute(f"INSERT INTO bio (`user id`) VALUES({userID})")
    mydb.commit()
    logging.info(f"Succesfully created user with email: {email}, user name: {name}, password: {password}")
    logging.info(f"new user created with email {email} and name {name}")
    '''
    except mysql.connector.errors.IntegrityError:
        logging.warning('User already exists')
    except:
        logging.error("Error creating new user")
    '''

def login(email, password):
    #try:
    cursor.execute(f"SELECT * FROM mydb.users WHERE email='{email}' AND password='{password}';")
    id = cursor.fetchall()[0][0]
    with open('credentials.txt', 'w') as f:
        credentials = str(id) + '\n' + email + '\n' + password
        f.write(credentials)
    logging.info(f"Succesfully logged in with email {email}")
    import functions_chat
    functions_chat.get_user(email)
    return 0
    '''
    except IndexError:
        return 1
    except:
        return 2
    '''