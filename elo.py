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
    data = file["data"]
    index = file["index"]
    data[index]["elo"], data[(index+1)%file["size"]]["elo"] = elo_update(data[index]["elo"], data[(index+1)%file["size"]]["elo"], winid)
    file["data"] = data
    file["lastmodified"] = str(datetime.now(timezone.utc))
    if (index+2)+1 > file["size"]:
        file["status"] = "STATIC"
        file["index"] = 0
        file = json.dumps(file)
        with open(path, 'w') as wpath:
            wpath.write(file)
            wpath.close()
        return "EOF"
    file["index"] += 2
    file = json.dumps(file)
    with open(path, 'w') as wpath:
        wpath.write(file)
        wpath.close()
    return "SUCCESS"

#key for sorting the list
def elo_key(item):
	return item['elo']

#contract: string->none
#sorts the list
def sort_list(list_name):
	list_name.sort(reverse=True,key=elo_key)

#contract: string,string -> none
#deletes an item from the specified ranked list
def delete_item(list_name,item_name):
	with open('userdata/testuser/lists/'+(list_name+'.json'),'r') as file:
		file = file.read()

	file = json.loads(file)
	file = file[list_name]

	for item in file:
		if item["name"] == item_name:
			file.remove(item)
	file = {list_name:file}
	file = json.dumps(file)

	with open('userdata/testuser/lists/'+(list_name+'.json'),'w') as data:
		data.write(file)
		data.close()


#contract: string,string -> none
#adds an item to the specified ranked list, then does two matches and sorts
def add_item(list_name,item_name):
	with open('userdata/testuser/lists/'+(list_name+'.json'),'r') as file:
		file = file.read()

	file = json.loads(file)
	file = file[list_name]

	file.append({"name":item_name,"elo":1500})

	opponents = random.sample(file[0:len(file)-1], 2)
	for opp in opponents:
		file[-1]["elo"], opp["elo"] = elo_update(item_name, file[-1]["elo"], opp["name"], opp["elo"])
	sort_list(file)

	file = {list_name:file}
	file = json.dumps(file)

	with open('userdata/testuser/lists/'+(list_name+'.json'),'w') as data:
		data.write(file)
		data.close()



#contract: none -> none
#makes + ranks list, then writes to json file
#UNCOMMENT THE FOLLOWING LINES TO TRY OUT THE FUNCTIONS

#new_list()
#delete_item(input("Name of list"),input("Item to delete"))
#add_item(input("Name of list"),input("Item to add"))
