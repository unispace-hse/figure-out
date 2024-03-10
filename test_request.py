import requests

url = "http://localhost:8282"

loadDict = {"new_material": 3, "pages": 2, "time": 30}
r = requests.get(url + "/get_task", params=loadDict)
print(r.text)

params = {"Q1": 1, "Q2": [5, 8, 6], "weights": 0.5}
response = requests.get(url + "/get_score", params=params)

print(response.text)

params = {"task": 0.6, "score": 0.5}

response = requests.get(url + "/get_rate", params=params)

print(response.text)

params = {"weight": 0.6, "weights": 2.5, "rate": 1.7, "daysLeft": 5}

response = requests.get(url + "/get_next_interval", params=params)

print(response.text)

params = {"Q3": [1, 4, 5], "T1": [1], "age": 18}

response = requests.get(url + "/get_habit", params=params, timeout=10)

print(response.text)

params = {
    "count_task": 10,
    "count_todos": 5,
    "count_habits": 4,
    "missed_events": 0,
    "events": [1],
    "reviewed": True,
}

response = requests.get(url + "/get_grade", params=params, timeout=10)

print(response.text)
