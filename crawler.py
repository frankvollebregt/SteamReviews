import requests
import json

URL = "https://store.steampowered.com/appreviews/582010"

PARAMS = {
    'json': 1,
    'cursor': '*',
    'day_range': 9223372036854775807
}

data = []

r = requests.get(url=URL, params=PARAMS)
data1 = r.json()

print("Found total matching results: "+ str(data1['query_summary']['total_reviews']))

print("retrieved "+str(len(data1['reviews']))+" reviews")
data.extend(data1['reviews'])

for i in range(100):
    r = requests.get(url=URL, params=PARAMS)
    data1 = r.json()

    PARAMS['cursor'] = data1['cursor']
    print("retrieved " + str(len(data1['reviews'])) + " more reviews")
    data.extend(data1['reviews'])

res = []
for i in data:
    if i not in res:
        res.append(i)


with open('data/data.txt', 'w') as outfile:
    json.dump(res, outfile)