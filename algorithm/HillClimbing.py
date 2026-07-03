import random

from algorithm.Algorithm import Algorithm, Tactic
from problem.problem import Problem
from problem.solution import Solution


class HillClimbing(Algorithm):
    def __init__(self, problem: Problem, tactic: Tactic, epochs: int, freeze: int):
        super().__init__(problem)
        self.tactic: Tactic = tactic
        self.epochs: int = epochs
        self.max_freeze: int = freeze

    def solve(self) -> Solution:
        current_solution = random.choice(
            [self.backward_greedy(), self.greedy_type_grouping(), self.marginal_cost_minimization()])
        current_solution_value = self.problem.calculate_cost_of_solution(current_solution)

        best_solution = current_solution
        best_solution_value = current_solution_value
        freeze = 0

        for epoch in range(self.epochs):
            neighbour = self.find_neighbour(current_solution_value, current_solution)

            if neighbour is None:
                freeze += 1
                if freeze >= self.max_freeze:
                    current_solution = random.choice(
                        [self.backward_greedy(), self.greedy_type_grouping(), self.marginal_cost_minimization()])
                    current_solution_value = self.problem.calculate_cost_of_solution(current_solution)
                    freeze = 0
                continue

            freeze = 0
            current_solution = neighbour
            current_solution_value = self.problem.calculate_cost_of_solution(neighbour)

            if current_solution_value < best_solution_value:
                best_solution = current_solution
                best_solution_value = current_solution_value

        return best_solution


    def find_neighbour(self, solution_cost: int, solution: Solution) -> Solution | None:
        s1 = [self.swap_operator(solution) for _ in range(10)]
        s2 = [self.move_operator(solution) for _ in range(30)]
        s3 = [self.deadline_based_swap(solution) for _ in range(20)]
        s4 = [self.adjacent_swap(solution) for _ in range(10)]

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

        def first_improving(neighbours: list[Solution | None]) -> Solution | None:
            random.shuffle(neighbours)

            for neighbour in neighbours:
                if neighbour is None:
                    continue

                neighbour_cost = self.problem.calculate_cost_of_solution(neighbour)
                if neighbour_cost < solution_cost:
                    return neighbour

            return None


        match self.tactic:
            case Tactic.BestImproving:
                return best_improving(s1 + s2 + s3 + s4)
            case Tactic.FirstImproving:
                return first_improving(s1 + s2 + s3 + s4)
            case _:
                raise ValueError("No such tactic")