#Database procesing code
import json
import os
from hashlib import sha256
from datetime import datetime, timezone

datapath = "userdata/" 

def verify_credentials(path, password):
    userpath = path + "/userdata.json"
    if os.path.exists(userpath) == False:
        return "NOPATH" 
    userdata = json.loads(open(userpath, 'r').read())
    if sha256(password.encode('utf-8')).hexdigest() == userdata["password"]:
        userdata["lastlogin"] = str(datetime.now(timezone.utc))
        with open(userpath, 'w') as wpath:
            wpath.write(json.dumps(userdata))
            wpath.close()
        return "SUCCESS" 
    else:
        return "INV_PASS" 

def create_account(userpath, password, cpassword):
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

def get_lists(path):
    userpath = path + "/lists/"
    if os.path.exists(userpath) == False:
        return "NOPATH"
    pathlist = os.listdir(userpath)
    for i in range(len(pathlist)):
        pathlist[i] = pathlist[i][:len(pathlist[i])-5]
    return pathlist

if __name__ == "__main__":
    print("attempting to run module as main")
