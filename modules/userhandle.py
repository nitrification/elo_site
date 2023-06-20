#Database processing code
import json
import os
from hashlib import sha256
from datetime import datetime, timezone

datapath = "../userdata/"

def verify_credentials(user, password):
    userpath = datapath + user + "/userdata.json"
    if os.path.exists(userpath) == False:
        return "NOPATH" 
    fp = open(userpath, 'r')
    userdata = json.loads(fp.read())
    fp.close()
    if sha256(password.encode('utf-8')).hexdigest() == userdata["password"]:
        userdata["lastlogin"] = str(datetime.now(timezone.utc))
        with open(userpath, 'w') as wpath:
            wpath.write(json.dumps(userdata))
            wpath.close()
        return "SUCCESS" 
    else:
        return "INV_PASS" 

def create_account(user, password, cpassword):
    userpath = datapath + user + "/"
    if os.path.exists(userpath) == True:
        return "DUPATH" 
    if password != cpassword:
        return "INV_PASS"
    os.mkdir(userpath)
    os.chmod(userpath, 0o777)
    os.mkdir(userpath + "lists")
    os.chmod(userpath + "lists", 0o777)
    userdata = {
            "username" : user,
            "password" : sha256(password.encode('utf-8')).hexdigest(),
            "lastlogin" : str(datetime.now(timezone.utc)),
            "accountcreated" : str(datetime.now(timezone.utc))
            }
    with open(userpath + "userdata.json", 'w') as wpath:
        wpath.write(json.dumps(userdata))
        wpath.close()
    return "SUCCESS" 

def get_lists(user):
    userpath = datapath + user + "/lists/"
    if os.path.exists(userpath) == False:
        return "NOPATH"
    return os.listdir(userpath)

if __name__ == "__main__":
    pass
