import mysql.connector 
import MySQLdb
import logging

mydb = mysql.connector.connect(host = '129.154.40.30', user = 'app', passwd = 'password', database = 'mydb')
cursor = mydb.cursor()
print(mydb)

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


def create_group(groupName, ownerID, participant1, participant2, *participantIDs):
    try:
        cursor.execute(f"INSERT INTO `groups` (`group name`) VALUES ('{groupName}')")
        id = cursor.lastrowid
        cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{participant1}', {id})")
        cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{participant2}', {id})")
        for x in participantIDs:
            cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{x}', {id})")
        mydb.commit()   
    except:
        logging.error("Couldn't create group")

def add_participant_to_group(groupID, participantID, *participantIDs):
    try:
        cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{participantID}', '{groupID}');")
        for x in participantIDs:
            cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{x}', '{groupID}');")
        mydb.commit()
    except:
        logging.error("Couldn't create group")

