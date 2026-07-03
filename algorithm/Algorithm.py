from abc import ABC, abstractmethod
import random

from problem.problem import Problem
from problem.solution import Solution


class Algorithm(ABC):
    def __init__(self, problem: Problem):
        self.problem = problem

    @abstractmethod
    def solve(self) -> Solution:
        pass

    def basic_solution(self) -> Solution:
        solution = [None] * self.problem.number_of_slots

        products = sorted(
            range(self.problem.products),
            key=lambda p: self.problem.due_time_slots[p]
        )

        for product in products:
            deadline = self.problem.due_time_slots[product] - 1

            for slot in range(deadline, -1, -1):
                if solution[slot] is None:
                    solution[slot] = product
                    break
            else:
                raise ValueError("No feasible schedule")

        return Solution(solution)


    def swap_operator(self, solution: Solution) -> Solution | None:
        tmp_solution = solution().copy()

        indices = [i for i, x in enumerate(tmp_solution) if x is not None]
        a, b = random.sample(indices, 2)

        tmp_solution[a], tmp_solution[b] = tmp_solution[b], tmp_solution[a]

        new_solution = Solution(tmp_solution)
        return new_solution if self.problem.is_solution_valid(new_solution) else None

    def move_operator(self, solution: Solution) -> Solution | None:
        tmp = solution().copy()

        indices = [i for i, x in enumerate(tmp) if x is not None]
        a, b = random.sample(indices, 2)

        job = tmp.pop(a)
        tmp.insert(b, job)

        new_solution = Solution(tmp)
        return new_solution if self.problem.is_solution_valid(new_solution) else None


    def deadline_based_swap(self, solution: Solution) -> Solution | None:
        tmp = solution().copy()

        jobs = [(i, job) for i, job in enumerate(tmp) if job is not None]
        if len(jobs) < 2:
            return None

        def slack(i, job):
            deadline = self.problem.due_time_slots[job] - 1
            return deadline - i

        bad = [i for i, j in jobs if slack(i, j) <= 0]
        good = [i for i, j in jobs if slack(i, j) > 0]

        if not bad or not good:
            bad, good = zip(*random.sample(jobs, 2))

        a = random.choice(bad)
        b = random.choice(good)

        tmp[a], tmp[b] = tmp[b], tmp[a]

        new_solution = Solution(tmp)
        return new_solution if self.problem.is_solution_valid(new_solution) else None
