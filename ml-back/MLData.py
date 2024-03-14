from random import shuffle
import json
import tensorflow as tf
import pickle
import math


def get_task(new_material, pages, time) -> float:
    with open("models/scalers/scaler_weight.pkl", "rb") as f:
        scaler = pickle.load(f)
        loaded_model = tf.keras.models.load_model("models/calculate_weight")
        input_features = scaler.transform([[new_material, pages, time]])
        return loaded_model.predict(input_features)[0][0]


def get_score(Q1, Q2, weights) -> float:
    s, d, p, u = 0, 0, 0, 0
    for i in Q2:
        if i <= 7:
            s += 1
        elif i <= 9:
            d += 1
        elif i <= 13:
            p += 1
        else:
            u += 1
    with open("models/scalers/scaler_score.pkl", "rb") as f:
        scaler = pickle.load(f)
        loaded_model = tf.keras.models.load_model("models/calculate_score")
        input_features = scaler.transform([[s, d, p, u, Q1]])
        return loaded_model.predict(input_features)[0][0]


def get_rate(task, score) -> float:
    with open("models/scalers/scaler_rate.pkl", "rb") as f:
        scaler = pickle.load(f)
        loaded_model = tf.keras.models.load_model("models/calculate_rate")
        input_features = scaler.transform([[task, score]])
        return loaded_model.predict(input_features)[0][0]


def get_next_interval(weight, weights, rate, daysLeft) -> int:
    if rate < 1.3:
        rate = 1.5
    if daysLeft == -1:
        return -1
    cutNumber = 60
    if daysLeft >= 60:
        return -1
    exceedLevel = max(1, weight)
    nextDay = math.ceil(min(daysLeft * rate, cutNumber * exceedLevel))
    return int(nextDay)


def get_habit(Q3, T1, age):
    age = 18  # TODO: Implement ages split
    pathHabits = (
        "data/Q3_a_marked.json" if age >= 12 and age <= 24 else "data/Q3_b_marked.json"
    )
    pathMap = "data/Q3_a_map.json" if age >= 12 and age <= 24 else "data/Q3_b_map.json"
    habits = json.load(open(pathHabits, "r"))
    pathMap = json.load(open(pathMap, "r"))
    shuffle(Q3)
    for bad_habit in Q3:
        for solution in pathMap[bad_habit - 1]["habits"]:
            if solution in T1:
                continue
            name = habits[solution - 1]["name"]
            type = habits[solution - 1]["type"]
            value = habits[solution - 1]["value"]
            return (name, type, value, solution)
    if T1 != []:
        return get_habit(Q3, [], age)
    else:
        return "Update an app. Cause there's a problem with habits suggestion"


def get_grade(count_task, count_todos, count_habits, missed_events, events, reviewed):
    if events == [-1]:
        events = []
    reviewed = True  # Delete when text added
    cntEvents = len(set(events))
    # "tasks", "habits", "todos", "cntEvents", "missed", "reviewed", "grade"
    with open("models/scalers/scaler_grade.pkl", "rb") as f:
        scaler = pickle.load(f)
        loaded_model = tf.keras.models.load_model("models/calculate_grade")
        input_features = scaler.transform(
            [
                [
                    count_task,
                    count_habits,
                    count_todos,
                    cntEvents,
                    missed_events,
                    reviewed,
                ]
            ]
        )
        grade = loaded_model.predict(input_features)[0][0]
        if missed_events == 0:
            grade = max(grade, 7)
            if count_task + count_todos + count_habits + cntEvents > 9:
                grade = max(grade, 8.5)
        elif missed_events == 1:
            grade = min(grade, 6.5)
            if count_task + count_todos + count_habits + cntEvents < 7:
                grade = 5
        elif missed_events == 2:
            grade = min(grade, 6)
            if count_task + count_todos + count_habits + cntEvents < 8:
                grade = 5
        elif missed_events == 3:
            grade = min(grade, 5)
        elif missed_events > 3:
            grade = min(grade, 4.5)
        return max(3, min(grade, 10))
