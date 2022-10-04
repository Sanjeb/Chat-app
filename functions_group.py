import logging
import connect

mydb = connect.mydb
cursor = connect.cursor

def create_group(groupName, ownerID, participant1, participant2, *participantIDs):
    try:
        cursor.execute(f"INSERT INTO `groups` (`group name`) VALUES ('{groupName}')")
        id = cursor.lastrowid
        cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{participant1}', {id})")
        cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{participant2}', {id})")
        for x in participantIDs:
            cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{x}', {id})")
        mydb.commit()   
        logging.info(f"Created new group {groupName}")
    except:
        logging.error("Couldn't create group")

def delete_group(groupID):
    try:
        cursor.execute(f"DELETE FROM `group messages` WHERE (`groups_group id` = '{groupID}')")
        cursor.execute(f"DELETE FROM `group members` WHERE (`groups_group id` = '{groupID}')")
        cursor.execute(f"DELETE FROM `groups` WHERE (`group id` = '{groupID}')")
        mydb.commit()
        logging.info(f"Deleted group with ID {groupID}")
    except:
        logging.error("Couldn't delete group")
    
def add_participant_to_group(groupID, participantID, *participantIDs):
    try:
        cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{participantID}', '{groupID}');")
        for x in participantIDs:
            cursor.execute(f"INSERT INTO `group members` (`users_user id`, `groups_group id`) VALUES ('{x}', '{groupID}');")
        mydb.commit()
        logging.info(f"Added participant {participantID} to group {groupID}")
    except:
        logging.error("Couldn't add participant to group")

def remove_participant_from_group(groupID, participantID, *participantIDs):
    try:
        cursor.execute(f"DELETE FROM `group members` WHERE (`users_user id` = '{participantID}') and (`groups_group id` = '{groupID}');")
        for x in participantIDs:
            cursor.execute(f"DELETE FROM `group members` WHERE (`users_user id` = '{x}') and (`groups_group id` = '{groupID}');")
        mydb.commit()
        logging.info(f"Removed participant {participantID} {participantIDs} from group {groupID}")
    except:
        logging.error("Couldn't remove participant from group")

