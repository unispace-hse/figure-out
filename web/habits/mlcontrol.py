from random import shuffle
import json


class MLData:
    def __init__(self):
        raise RuntimeError("Cannot instantiate a static class")

    @staticmethod
    def get_task(new_material, pages, time) -> float:
        return 0.8

    @staticmethod
    def get_score(Q1, Q2, weights) -> float:
        return 0.5

    @staticmethod
    def get_rate(task, score) -> float:
        return 1.5

    @staticmethod
    def get_next_interval(weight, weights, rate, daysLeft) -> int:
        return 4

    @staticmethod
    def get_habit(Q3, T1, age):
        age = 18  # TODO: Implement ages split
        pathHabits = (
            "habits/data/Q3_a_marked.json"
            if 12 <= age <= 24
            else "habits/data/Q3_b_marked.json"
        )
        path_map = (
            "habits/data/Q3_a_map.json" if age >= 12 and age <= 24 else "habits/data/Q3_b_map.json"
        )
        habits = json.load(open(pathHabits, "r"))
        path_map = json.load(open(path_map, "r"))
        shuffle(Q3)
        for bad_habit in Q3:
            for solution in path_map[bad_habit - 1]["habits"]:
                if solution in T1:
                    continue
                name = habits[solution - 1]["name"]
                type = habits[solution - 1]["type"]
                value = habits[solution - 1]["value"]
                return (name, type, value, solution)
        if T1 != []:
            return MLData.get_habit(Q3, [], age)
        else:
            return "Update an app. Cause there's a problem with habits suggestion"

    @staticmethod
    def get_grade(
        count_task, count_todos, count_habits, missed_events, events=None, reviewed=None
    ):
        return 9.5


class Compute:
    def __init__(self):
        raise RuntimeError("Cannot instantiate a static class")

    @staticmethod
    def get_sl_data(
        new_material, pages, time, Q1, Q2, weights
    ) -> tuple[float, float, int]:
        task_weight = MLData.get_task(new_material, pages, time)
        user_score = MLData.get_score(Q1, Q2, weights)
        rate = MLData.get_rate(task_weight, user_score)
        daysLeft = MLData.get_next_interval(
            task_weight, weights + task_weight, rate, 0.8
        )
        return (task_weight, rate, daysLeft)

    @staticmethod
    def get_sl_recap(
        rate, weights, weight, daysLeft, answer
    ) -> tuple[float, float, int]:
        if answer == 0:
            weights -= weight
            weight *= 0.86
            weights += weight
            next_rep = MLData.get_next_interval(weight, weights, rate, daysLeft)
            return (weight, rate, next_rep)
        if answer == 1:
            next_rep = MLData.get_next_interval(weight, weights, rate, daysLeft)
            return (weight, rate, next_rep)
        weight *= 1.1
        rate *= 0.9
        return (weight, rate, daysLeft)

    @staticmethod
    def get_habit(Q3, T1, age=18) -> tuple[str, str, int, int]:
        return MLData.get_habit(Q3, T1, age)

    @staticmethod
    def get_grade(
        count_task, count_todos, count_habits, missed_events, events=None, reviewed=None
    ) -> float:
        return MLData.get_grade(
            count_task, count_todos, count_habits, missed_events, events, reviewed
        )
