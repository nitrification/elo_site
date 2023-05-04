import random
master_list = []

#make the list
def make_list():
	ranking_list = []
	make_list = True
	i = 0
	while make_list:
		name = input("Enter name of item to rank, or type 'done' to finish ")
		if name.lower() == "done":
			break
		elo = 1500
		rank = None
		item_id = i
		item = {"name": name, "elo": elo, "item_id": item_id}
		ranking_list.append(item)
		i += 1
	return ranking_list

#find expected result
def expected_result(self_elo, foe_elo):
    return 1 / (1 + 10**((foe_elo - self_elo)/400))

#find new rating
def elo_update(name_1, elo_1, name_2, elo_2):
	K=30
	expected = expected_result(elo_1, elo_2)
	result = int(input("Which do you prefer? Type '1' for " + name_1 + " and type '0' for " + name_2 + " "))
	return elo_1 + K*(result - expected), elo_2 + K*((1 - result) - (1 - expected))

#match up 2 dictionary entries
def matchup(list_name):
    for i, dict in enumerate(list_name):
        opponents = random.sample(list_name[:i] + list_name[i+1:], 2)
        for opp in opponents:
            dict["elo"], opp["elo"] = elo_update(dict["name"], dict["elo"], opp["name"], opp["elo"])

#key for sorting the list
def elo_key(item):
	return item['elo']

#sort the list
def sort_list(list_name):
	list_name.sort(reverse=True,key=elo_key)

#do the thing
cool_list = make_list()
for item in cool_list:
	print(item)
matchup(cool_list)
sort_list(cool_list)
for item in cool_list:
	print(item)
master_list.append(cool_list)
#print(master_list)