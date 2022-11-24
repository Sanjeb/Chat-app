import logging
import connect

mydb = connect.mydb
cursor = connect.cursor


with open('credentials.txt', 'r') as f:
    CurrentUserID, email, password = f.read().split()


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

def get_dm_messages(dmID):
    cursor.execute(f"SELECT `dm messages`.*, users.`user name` FROM `dm messages`, users  WHERE `dm id` = {dmID} AND `sender user id` = users.`user id` ORDER BY `time sent`;")
    messages = []
    for x in cursor:
        messages.append(x)
    return messages #Returns list in the format [(MessageID, MessageText, SenderUserID, DMID, SenderUsername), (MessageID, MessageText, SenderUserID, DMID, SenderUsername)]

def get_latest_dm_messages(dmID, lastMessageID):
    cursor.execute(f"SELECT `dm messages`.*, users.`user name` FROM `dm messages`, users WHERE `message id` > {lastMessageID} AND `dm id` = {dmID} AND `sender user id` = users.`user id` ORDER BY `time sent`;")
    messages = []
    for x in cursor:
        messages.append(x)
    return messages #Returns list in the format [(MessageID, MessageText, SenderUserID, DMID, SenderUsername), (MessageID, MessageText, SenderUserID, DMID, SenderUsername)]

def get_dm_users():
    cursor.execute(f"SELECT * FROM `dm members` WHERE `user id` = {CurrentUserID}")
    ids = []
    dms = cursor.fetchall()
    for x in dms:
        cursor.execute(f" SELECT `dm members`.*, users.`user name` FROM `dm members`, users WHERE `dm members`.`dm id` = {x[1]} and `dm members`.`user id` != {CurrentUserID} AND `dm members`.`user id` = `users`.`user id`;")
        dm_ids = cursor.fetchall()
        ids.append(dm_ids[0])
    return ids #Returns list in the format [(UserID, DMID, UserName), (UserID, DMID, UserName)]
 
def send_dm_messages(dmID, message):
    cursor.execute(f"INSERT INTO `dm messages` (`message text`, `sender user id`, `dm id`) VALUES ('{message}', '{CurrentUserID}', '{dmID}');")
    mydb.commit()