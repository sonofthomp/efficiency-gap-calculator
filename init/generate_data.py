import csv
import json

f = open('../static/data/vote_counts/1976-2020-house.csv')
data = list(csv.reader(f, delimiter=','))

districts = {}

for line in data:
	party = line[12]
	if party not in ["DEMOCRAT", "REPUBLICAN"]:
		continue

	state = line[2]
	district = str(int(line[7]))
	vote_count = int(line[15])
	if district == "0":
		district = "At Large"

	if state not in districts.keys():
		districts[state] = {}
	if district not in districts[state].keys():
		districts[state][district] = {}

	districts[state][district][party[0]] = int(vote_count)
	districts[state][district]["TOTAL"]  = int(line[16])

for state in districts:
	for district in districts[state]:
		if 'D' not in districts[state][district]:
			districts[state][district]['D'] = districts[state][district]['TOTAL'] - districts[state][district]['R']
		if 'R' not in districts[state][district]:
                        districts[state][district]['R'] = districts[state][district]['TOTAL'] - districts[state][district]['D']
                        print(state, district, districts[state][district])

print(districts)

with open('../static/data/vote_counts.json', 'w') as f:
	f.write(json.dumps(districts, indent=4))
