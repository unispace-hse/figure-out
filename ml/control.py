# prompt: static class computing
import MLData

class Compute:
    def __init__(self):
        raise RuntimeError('Cannot instantiate a static class')

    @staticmethod
    def get_sl_data(new_material, pages, time, Q1, Q2, weights) -> tuple[float, float, int]:
      task_weight = MLData.get_task(new_material, pages, time)
      user_score = MLData.get_score(Q1, Q2, weights)
      rate = MLData.get_rate(task_weight, user_score)
      daysLeft = MLData.get_next_interval(task_weight, weights + task_weight, rate, 0.8)
      return (task_weight, rate, daysLeft)
    
    @staticmethod
    def get_sl_recap(rate, weights, weight, daysLeft, answer) -> tuple[float, float, int]:
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
    def get_habit(Q3, T1, age = 18) -> tuple[str, str, int, int]:
      return MLData.get_habit(Q3, T1, age)

    @staticmethod
    def get_grade(count_task, count_todos, count_habits, missed_events, events = None, reviewed = None) -> float:
      return MLData.get_grade(count_task, count_todos, count_habits, missed_events, events, reviewed)
