from enum import Enum

from algorithm.Algorithm import Algorithm
from problem.problem import Problem
from problem.solution import Solution

class Tactic(Enum):
    BestImproving = 0


class HillClimbing(Algorithm):
    def __init__(self, problem: Problem, epochs: int, tactic: Tactic):
        super().__init__(problem)
        self.epochs: int = epochs
        self.tactic = tactic


    def solve(self) -> Solution:
        basic_solution = self.basic_solution()

        best_solution = basic_solution
        best_solution_value = self.problem.calculate_cost_of_solution(best_solution)

        for epoch in range(self.epochs):
            neighbour = self.find_neighbour(best_solution_value, best_solution)

            if neighbour is None:
                continue

            neighbour_cost = self.problem.calculate_cost_of_solution(neighbour)
            if neighbour_cost < best_solution_value:
                best_solution = neighbour
                best_solution_value = neighbour_cost

        return best_solution


    def find_neighbour(self, solution_cost: int, solution: Solution) -> Solution | None:
        s1 = [self.swap_operator(solution) for _ in range(10)]
        s2 = [self.move_operator(solution) for _ in range(30)]
        s3 = [self.deadline_based_swap(solution) for _ in range(20)]

        def best_improving(neighbours: list[Solution | None]) -> Solution | None:
            best_solution = None
            smallest_cost = solution_cost

            for neighbour in neighbours:
                if neighbour is None:
                    continue

                neighbour_cost = self.problem.calculate_cost_of_solution(neighbour)
                if neighbour_cost < smallest_cost:
                    smallest_cost = neighbour_cost
                    best_solution = neighbour

            return best_solution


        match self.tactic:
            case Tactic.BestImproving:
                return best_improving(s1 + s2 + s3)
            case _:
                raise ValueError("No such tactic")