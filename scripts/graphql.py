import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os
APIKEY=os.getenv('TOKEN_MDC')
headers={ 'Content-Type':'application/json', 'Authorization':APIKEY }

apiUrl = "https://api.monday.com/v2"
query = 'query { items {id}}'
data = {'query' : query}

r = requests.post(url=apiUrl, json=data, headers=headers) # make request
print(r.json())