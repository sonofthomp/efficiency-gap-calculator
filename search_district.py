#!/usr/bin/python3
print("Content-Type: text/html\n")
print("")

import cgi
import cgitb
import json
from jinja2 import Template, Environment, FileSystemLoader

def fs2d():
	'''
	Convert return val of FieldStorage() into standard dictionary
	'''
	d = {}
	L = []
	formData = cgi.FieldStorage()
	for k in formData.keys():
		d[k] = formData[k].value
	return d

cgitb.enable()
info = fs2d()
state = info['state']
if 'district' in info:
	district = info['district']

data = json.loads(open('static/data/vote_counts/vote_counts.json', 'r').read())
relevant = data[state]
total_d = 0
total_r = 0
total_d_wasted = 0
total_r_wasted = 0

for district in relevant:
	total_d += relevant[district]['D']
	total_r += relevant[district]['R']
	if relevant[district]['D'] > relevant[district]['R']:
		relevant[district]['D_WASTED'] = relevant[district]['D'] - ((relevant[district]['D'] + relevant[district]['R']) // 2)
		relevant[district]['R_WASTED'] = relevant[district]['R']
	else:
                relevant[district]['D_WASTED'] = relevant[district]['D']
                relevant[district]['R_WASTED'] = relevant[district]['R'] - ((relevant[district]['D'] + relevant[district]['R']) // 2)
	total_d_wasted += relevant[district]['D_WASTED']
	total_r_wasted += relevant[district]['R_WASTED']

totals = {"D": total_d, 'R': total_r, 'D_WASTED': total_d_wasted, 'R_WASTED': total_r_wasted}
efficiency_gap = abs(round(100 * (totals['D_WASTED'] - totals['R_WASTED']) / (totals['D'] + totals['R']), 2))
percent_contribution = round(100 * (total_d - total_r) / (total_d + total_r), 2)

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('search_district.html')

minus_limit = round(efficiency_gap - 7, 2)
state_unabbreivated = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}[state]

print(template.render(state_unabbreviated=state_unabbreivated, minus_limit = minus_limit, votes=relevant, state=info['state'], total_d=totals['D'], total_r=totals['R'], wasted_d=totals['D_WASTED'], wasted_r=totals['R_WASTED'], gap=efficiency_gap, percent=percent_contribution))
