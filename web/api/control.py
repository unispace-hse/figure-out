# prompt: static class computing
import math
from . import transmitter


def get_sl_data(new_material, pages, time, Q1, Q2, weights) -> tuple[float, float, int]:
    task_weight = transmitter.get_task(new_material, pages, time)
    user_score = transmitter.get_score(Q1, Q2, weights)
    rate = transmitter.get_rate(task_weight, user_score)
    daysLeft = transmitter.get_next_interval(
        task_weight, weights + task_weight, rate, 0.8
    )
    return task_weight, rate, daysLeft


def get_sl_recap(rate, weights, weight, daysLeft, answer) -> tuple[float, float, int]:
    if answer == 0:
        weights -= weight
        weight *= 0.86
        weights += weight
        rate *= 1.15
        next_rep = transmitter.get_next_interval(weight, weights, rate, daysLeft)
        return weight, rate, next_rep
    if answer == 1:
        return weight, rate, math.ceil(daysLeft + rate)
    weight *= 1.1
    rate *= 0.9
    return weight, rate, math.ceil(daysLeft / rate)


def get_habit(Q3, T1, age=18) -> tuple[str, str, int, int]:
    return transmitter.get_habit(Q3, T1, age)


def get_grade(
    count_task, count_todos, count_habits, missed_events, events=None, reviewed=True
) -> float:
    if events is None:
        events = [-1]
    return transmitter.get_grade(
        count_task, count_todos, count_habits, missed_events, events, reviewed
    )
