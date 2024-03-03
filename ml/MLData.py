from random import shuffle
import json

class MLData:
  def __init__(self):
    raise RuntimeError('Cannot instantiate a static class')

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
    age = 18 # TODO: Implement ages split
    pathHabits = "data/Q3_a_marked.json" if age >= 12 and age <= 24 else "data/Q3_b_marked.json"
    pathMap = "data/Q3_a_map.json" if age >= 12 and age <= 24 else "data/Q3_b_map.json"
    habits = json.load(open(pathHabits, 'r'))
    pathMap = json.load(open(pathMap, 'r'))
    shuffle(Q3)
    for bad_habit in Q3:
      for solution in pathMap[bad_habit - 1]["habits"]:
        if solution in T1:
            continue
        name = habits[solution - 1]["name"]
        type = habits[solution - 1]["type"]
        value = habits[solution - 1]["value"]
        return (name, type, value, solution)
    if (T1 != []): 
        return MLData.get_habit(Q3, [], age)
    else:
        return ("Update an app. Cause there's a problem with habits suggestion")
      
  
  @staticmethod
  def get_grade(count_task, count_todos, count_habits, missed_events, events = None, reviewed = None):
    return 9.5
