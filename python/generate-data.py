import csv

f = open('../data/voting-history/1976-2020-house.csv')
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

print(districts)