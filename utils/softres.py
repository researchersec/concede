import json
import requests

with open("gargulexport.json", "r", encoding="utf-8") as f:
    data = json.load(f)

softres_ids = sorted({
    entry["softresID"]
    for entry in data
    if "softresID" in entry
})

print(softres_ids)


for softres_id in softres_ids:
  print(softres_id)
  print(f"getting softres data from api for ID: {softres_id} ......")
  response = requests.get(f"https://softres.it/api/raid/{softres_id}")
  if response.status_code == 200:
    try:
      response_data = response.json()
      filename = f"softres/{softres_id}.json"
      with open(filename, "w", encoding="utf-8") as f:
        json.dump(response_data, f, indent=4)
      print(f"Successfully saved data to {filename}")
    except json.JSONDecodeError:
      print(f"Error decoding JSON for {softres_id}: {response.text}")
  else:
    print(f"Error fetching data for {softres_id}: Status Code {response.status_code}")
