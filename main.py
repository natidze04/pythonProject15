import requests

import json

import sqlite3

import win10toast as win10toast

import win10toast


key = '0wadcVu2ObWjwJqn0uF3ATj7F2O0AaCVsBdVJc6U'

response = requests.get('https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=DEMO_KEY')

print(response)

result = response.json()

print(json.dumps(result, indent=4))

status_code = response.status_code

print("Status Code:", status_code)

headers = response.headers

print(headers)

with open('data.json', 'w') as json_file:

    json.dump(result, json_file, indent=4)

print("Data stored in data.json file.")

print(result['page']['size'])



page_size = result['page']['total_elements']

print(page_size)

near_earth_objects = result['near_earth_objects']
first_neo = near_earth_objects[0]
name = first_neo['name']
is_potentially_hazardous = first_neo['is_potentially_hazardous_asteroid']

print("First NEO Name:", name)
print("Is Potentially Hazardous?:", is_potentially_hazardous)

conn = sqlite3.connect('neos.db')

cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS neos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    is_potentially_hazardous INTEGER
                )''')


cursor.execute('''INSERT INTO neos (name, is_potentially_hazardous)
                VALUES (?, ?)''', (name, is_potentially_hazardous))


conn.commit()
conn.close()

from win10toast import ToastNotifier




toaster = ToastNotifier()

notification_title = "NEO Information"

notification_message = f"Name: {name}\nIs Potentially Hazardous?: {is_potentially_hazardous}"

toaster.show_toast(notification_title, notification_message, duration=10)

