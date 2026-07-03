from algorithm.Algorithm import Algorithm
from problem.problem import Problem
from problem.solution import Solution

import random
import math


class SimulatedAnnealing(Algorithm):
    temp: float
    temp_initial: float
    alfa: float
    max_stagnation: int
    reheats: int
    inner_iterations: int

    def __init__(self, problem: Problem, temp: float, alfa: float, max_stagnation: int, reheats: int, inner_iterations: int):
        super().__init__(problem)
        self.temp_initial = temp
        self.temp = temp
        self.alfa = alfa
        self.max_stagnation = max_stagnation
        self.reheats = reheats
        self.inner_iterations = inner_iterations

    def _reheat(self) -> None:
        self.temp = self.temp_initial * 0.4
        self.reheats -= 1

    def solve(self) -> Solution:
        current_solution = random.choice(
            [self.backward_greedy(), self.greedy_type_grouping(), self.marginal_cost_minimization()])
        current_solution_value = self.problem.calculate_cost_of_solution(current_solution)

        best_solution = current_solution
        best_solution_value = current_solution_value

        inner_iterations = self.inner_iterations
        stagnation_counter = 0

        while self.temp > 1e-4:
            improved_in_this_temp = False

            valid_evaluations = 0
            while valid_evaluations < inner_iterations:
                potential_solution = self.find_neighbour(current_solution)

                if potential_solution is None:
                    continue

                valid_evaluations += 1

                potential_solution_value = self.problem.calculate_cost_of_solution(potential_solution)

                delta_e = potential_solution_value - current_solution_value

                if delta_e < 0 or random.random() < math.exp(-delta_e / self.temp):
                    current_solution = potential_solution
                    current_solution_value = potential_solution_value

                    if current_solution_value < best_solution_value:
                        best_solution = potential_solution
                        best_solution_value = current_solution_value
                        improved_in_this_temp = True
                        stagnation_counter = 0

            self.temp *= self.alfa

            if not improved_in_this_temp:
                stagnation_counter += 1

            if stagnation_counter >= self.max_stagnation and self.reheats > 0:
                self._reheat()

                current_solution = best_solution
                current_solution_value = best_solution_value

                stagnation_counter = 0

        return best_solution

    def find_neighbour(self, solution: Solution) -> Solution | None:
        operator = random.choices(
            population=[self.swap_operator, self.move_operator, self.deadline_based_swap, self.adjacent_swap],
            weights=[10, 30, 20, 10],
            k=1
        )[0]

        return operator(solution)