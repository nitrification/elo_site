#make the list
def make_list():
	ranking_list = []
	make_list = True
	i = 0
	while make_list:
		name = input("Enter name of item to rank, or type 'done' to finish")
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
	K=15
	expected = expected_result(elo_1, elo_2)
	result = int(input("Which do you prefer? Type '1' for " + name_1 + " and type '0' for " + name_2))
	return elo_1 + K*(result - expected), elo_2 + K*((1 - result) - (1 - expected))

#match up 2 dictionary entries
def matchup(list_name):
	for i in range(len(list_name)):
		for j in range(i+1, len(list_name)):
			list_name[i]["elo"], list_name[j]["elo"] = elo_update(list_name[i]["name"],list_name[i]["elo"],list_name[j]["name"],list_name[j]["elo"])

#do the thing
cool_list = make_list()
for item in cool_list:
 	print(item)
matchup(cool_list)
for item in cool_list:
	print(item)
