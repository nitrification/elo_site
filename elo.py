import random
import json
import pprint

#contract:none->list
#make the list
def make_list():
	ranking_list = []
	make_list = True

	while make_list:
		name = input("Enter name of item to rank, or type 'done' to finish ")
		if name.lower() == "done":
			break
		elo = 1500
		rank = None
		item = {"name": name, "elo": elo}
		ranking_list.append(item)
	return ranking_list

#contract:int,int->int
#find expected result
def expected_result(self_elo, foe_elo):
    return 1 / (1 + 10**((foe_elo - self_elo)/400))

#contract:string,int,string,int->int,int
#find new rating
def elo_update(name_1, elo_1, name_2, elo_2):
	K=30
	expected = expected_result(elo_1, elo_2)
	result = int(input("Which do you prefer? Type '1' for " + name_1 + " and type '0' for " + name_2 + " "))
	return elo_1 + K*(result - expected), elo_2 + K*((1 - result) - (1 - expected))

#contract: string->none
#match up 2 dictionary entries
def matchup(list_name):
    for i, dict in enumerate(list_name):
        opponents = random.sample(list_name[:i] + list_name[i+1:], 2)
        for opp in opponents:
            dict["elo"], opp["elo"] = elo_update(dict["name"], dict["elo"], opp["name"], opp["elo"])

#contract: string->none
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
def new_list():
	cool_dict = make_list()
	dict_name = input("Enter list name ")
	matchup(cool_dict)
	sort_list(cool_dict)
	new_json = json.dumps({dict_name:cool_dict})
	with open('userdata/testuser/lists/'+(dict_name+'.json'),'w') as data:
		data.write(new_json)
		data.close()

#UNCOMMENT THE FOLLOWING LINES TO TRY OUT THE FUNCTIONS

#new_list()
#delete_item(input("Name of list"),input("Item to delete"))
#add_item(input("Name of list"),input("Item to add"))