import random
import json
import os
from datetime import datetime, timezone

#accepts a string which is the items in a list
#each entry is seperated by a \n character
#make_list(string data)
def make_list(path, id, data):
    if os.path.exists(path):
        return "DUPATH"
    file = {}
    file["id"] = id
    file["status"] = "STATIC"
    file["index"] = 0
    file["data"] = {}
    for i in data.split("\n"):
        file["data"][i] = 1500
    file["pairs"] = []
    file["pair_n"] = 0
    file["size"] = len(file["data"])
    file["lastmodified"] = str(datetime.now(timezone.utc))
    with open(path, 'w') as wpath:
        wpath.write(json.dumps(file))
        wpath.close()

#find expected result
#expected_result(int self_elo, int foe_elo)
def expected_result(self_elo, foe_elo):
    return 1 / (1 + 10**((foe_elo - self_elo)/400))

#contract:string,int,string,int->int,int
#find new rating
#result = 1 = elo1 win, reulst = 0 = elo2 win
def elo_update(elo_1, elo_2, result):
	K=30
	expected = expected_result(elo_1, elo_2)
	return round(elo_1 + K*(result - expected), 2), round(elo_2 + K*((1 - result) - (1 - expected)), 2)

#scramble the list for matchup
#scrample(filepath)
def make_pairs(path):
    if os.path.exists(path) == False:
        return "NOPATH"
    file = json.loads(open(path, 'r').read())
    if file["status"] != "STATIC":
        return "BUSY"
    data, size = file["data"], file["size"]
    pairs = []
    keylist = list(data.keys())
    random.shuffle(keylist)
    for i in range(0, size, 2):
        pairs.append([keylist[i], keylist[(i+1)%size]])

    file["lastmodified"] = str(datetime.now(timezone.utc))
    file["pairs"] = pairs
    file["pair_n"] = len(pairs)
    file["index"] = 0
    with open(path, 'w') as wpath:
        wpath.write(json.dumps(file))
        wpath.close()
        
    return "SUCCESS"

def get_pair(path):
    if os.path.exists(path) == False:
        return "NOPATH"
    file = json.loads(open(path, 'r').read())
    pair, index = file["pairs"], file["index"]
    return pair[index]

#updates the list, happens in packets
def update_list(path, winid):
    if os.path.exists(path) == False:
        return "NOPATH"
    file = json.loads(open(path, 'r').read())
    data, index, pair, pair_n = file["data"], file["index"], file["pairs"], file["pair_n"]
    pair = pair[index]
    data[pair[0]], data[pair[1]] = elo_update(data[pair[0]], data[pair[1]], winid)
    file["lastmodified"] = str(datetime.now(timezone.utc))

    if ((index+1) >= pair_n):
        file["index"] = 0
        with open(path, 'w') as wfile:
            wfile.write(json.dumps(file))
            wfile.close()
        return "END_OF_LIST"

    else:
        file["index"] += 1
        with open(path, 'w') as wfile:
            wfile.write(json.dumps(file))
            wfile.close()
        return "SUCCESS"



#EMPTY = NOTHING MORE TO DELETE
#INVALID_ID = ID DOESNT EXIST
#BUSY = FILE BEING USED BY SOMETHING else:
def delete_item(path, id):
    if os.path.exists(path) == False:
        return "NOPATH"
    file = json.loads(open(path, 'r').read())
    if file["status"] != "STATIC":
        return "BUSY"

    data, size = file["data"],  file["size"]

    if size < 1:
        return "EMPTY"
    if id not in data:
        return "INVALID_ID"

    del data[id]
    size -= 1
    file["lastmodified"] = str(datetime.now(timezone.utc))

    with open(path, 'w') as wfile:
        wfile.write(json.dumps(file))
        wfile.close()

    return "SUCCESS"

#REDUN_ID = ID ALREADY EXISTS
#BUSY = FILE IS BEING USED BY SOMETHING ELSE
def add_item(path, id):
    if os.path.exists(path) == False:
        return "NOPATH"
    file = json.loads(open(path, 'r').read())
    if file["status"] != "STATIC":
        return "BUSY"

    data = file["data"]

    if id in data:
        return "REDUN_ID"

    data[id] = 1500
    file["size"] = len(data) 
    file["lastmodified"] = str(datetime.now(timezone.utc))

    with open(path, 'w') as wfile:
        wfile.write(json.dumps(file))
        wfile.close()

    return "SUCCESS"

def sort_list(path):
    if os.path.exists(path) == False:
        return "NOPATH"
    file = json.loads(open(path, 'r').read())
    if file["status"] != "STATIC":
        return "BUSY"
    file["data"] = dict(sorted(file["data"].items(), key=lambda i: i[1], reverse=True))
    file["lastmodified"] = str(datetime.now(timezone.utc))

    with open(path, 'w') as wfile:
        wfile.write(json.dumps(file))
        wfile.close()

    return "SUCCESS"

def view_list(path):
    if os.path.exists(path) == False:
        return "NOPATH"
    file = json.loads(open(path, 'r').read())
    if file["status"] != "STATIC":
        return "BUSY"
    return file["data"]

