import json
import random
import uuid
import os

os.remove('ads.json')

ads = {
  "ads": []
}

countries = None

with open('codes/countries.json', 'r') as f:
  countries = json.loads(''.join(f.readlines()))

for i in range(100):
  random_country = countries[random.randint(0, len(countries) - 1)]
  country_name = random_country['alpha2']
  
  if len(random_country['languages']) == 0: 
    continue
  
  language = random_country['languages'][0]

  ad = {
    "id": uuid.uuid4().hex,
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "country": country_name,
    "lang": language,
    "start_hour": random.randint(0, 23),
    "end_hour": random.randint(0, 23)
  }
  
  ads['ads'].append(ad)

with open('ads.json', 'w') as f:
  f.write(json.dumps(ads))