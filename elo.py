import random
import json
import pprint

from datetime import datetime, timezone

#accepts a string which is the items in a list
#each entry is seperated by a \n character
#make_list(string data)
def make_list(rawdata):
    namelist = rawdata.split("\n")
    for name in namelist:
        name = {"name" : name, "elo" : 1500}
    return namelist 

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
	return elo_1 + K*(result - expected), elo_2 + K*((1 - result) - (1 - expected))

#scramble the list for matchup
#scrample(filepath)
def scramble(path):
    file = json.loads(open(path, 'r').read())
    file["status"] = "UPDATE"
    file["index"] = 0
    file["data"] = random.shuffle(file["data"])
    file["lastmodified"] = str(datetime.now(timezone.utc))
    file = json.dumps(file)
    with open(path, 'w') as wpath:
        wpath.write(file)
        wpath.close()
    return

#updates the list, happens in packets
def update_list(path, winid):
    file = json.loads(open(path, 'r').read())
    if (file["status"] != "UPDATE"):
        return "NOT_UPDATE_MODE" 

    data, index, size = file["data"], file["index"], file["size"]
    data[index]["elo"], data[(index+1)%size]["elo"] = elo_update(data[index]["elo"], data[(index+1)%size]["elo"], winid)
    file["lastmodified"] = str(datetime.now(timezone.utc))

    if (index+2)+1 > size:
        file["status"], file["index"] = "STATIC", 0
        data = sorted(data, reverse=True, key=lambda k: k['elo'])
        with open(path, 'w') as wfile:
            wfile.write(json.dumps(file))
            wfile.close()
        return "END_OF_LIST"
    else:
        file["index"] += 2
        with open(path, 'w') as wfile:
            wfile.write(json.dumps(file))
            wfile.close()
        return "SUCCESS"

#contract: string,string -> none
#deletes an item from the specified ranked list
def delete_item(path, id):
    file = json.loads(open(path, 'r').read())
    data = file["data"]
    if any(id in i for i in data):

	
#contract: string,string -> none
#adds an item to the specified ranked list, then does two matches and sorts
def add_item(path, id):
	
#contract: none -> none
#makes + ranks list, then writes to json file
#UNCOMMENT THE FOLLOWING LINES TO TRY OUT THE FUNCTIONS

#new_list()
#delete_item(input("Name of list"),input("Item to delete"))
#add_item(input("Name of list"),input("Item to add"))
