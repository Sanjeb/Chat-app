import logging
import main

mydb = main.mydb
cursor = main.cursor


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
        logging.error("Couldn't add participant")