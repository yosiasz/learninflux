import requests

endpoint = "http://localhost:3000/api/dashboards/home"
data = {"ip": "1.1.2.3"}
headers = {"Authorization": "Bearer eyJrIjoiQ0s5VTBrV0tmaTgxeENMZlpQNlpNcjBlSlBxS3lKZDgiLCJuIjoicHl0aG9uIiwiaWQiOjF9"}

print(requests.get(endpoint, headers=headers).json())