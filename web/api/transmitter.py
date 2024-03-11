import json
import requests

url = "http://ml_app:8282"


def get_task(new_material, pages, time) -> float:
    params = {"new_material": new_material, "pages": pages, "time": time}
    response = requests.get(url + "/get_task", params=params, timeout=10)
    response_dict = json.loads(response.text)
    return float(response_dict["result"])


def get_score(Q1, Q2, weights) -> float:
    if not Q2:
        Q2 = [1]
    params = {"Q1": Q1, "Q2": Q2, "weights": weights}
    response = requests.get(url + "/get_score", params=params, timeout=10)
    response_dict = json.loads(response.text)
    return float(response_dict["result"])


def get_rate(task, score) -> float:
    params = {"task": task, "score": score}
    response = requests.get(url + "/get_rate", params=params, timeout=10)
    response_dict = json.loads(response.text)
    return float(response_dict["result"])


def get_next_interval(weight, weights, rate, daysLeft) -> int:
    params = {
        "weight": str(weight),
        "weights": str(weights),
        "rate": str(rate),
        "daysLeft": str(daysLeft),
    }
    response = requests.get(url + "/get_next_interval", params=params, timeout=10)
    response_dict = json.loads(response.text)
    return int(response_dict["result"])


def get_habit(Q3, T1, age):
    if not Q3:
        Q3 = [1]
    if not T1:
        T1 = [-1]
    params = {"Q3": Q3, "T1": T1, "age": age}
    response = requests.get(url + "/get_habit", params=params, timeout=10)
    response_dict = json.loads(response.text)
    return (
        response_dict["name"],
        response_dict["type"],
        int(response_dict["value"]),
        response_dict["solution"],
    )


def get_grade(
    count_task, count_todos, count_habits, missed_events, events=None, reviewed=True
):
    if events is None or not events:
        events = [-1]
    params = {
        "count_task": count_task,
        "count_todos": count_todos,
        "count_habits": count_habits,
        "missed_events": missed_events,
        "events": events,
        "reviewed": reviewed,
    }
    response = requests.get(url + "/get_grade", params=params, timeout=10)
    response_dict = json.loads(response.text)
    return float(response_dict["result"])
