from algorithm.Algorithm import Algorithm
from problem.problem import Problem
from problem.solution import Solution

import random
import math
import numpy as np
import copy


class SimulatedAnnealing(Algorithm):
    temp: float
    temp_initial: float
    alfa: float
    max_stagnation: int
    reheats: int
    inner_iterations: int

    def __init__(
        self,
        problem: Problem,
        temp: float,
        alfa: float,
        max_stagnation: int,
        reheats: int,
        inner_iterations: int,
    ):
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

    def _run(self) -> Solution:
        current_solutions = [
            self.backward_greedy(),
            self.greedy_type_grouping(),
            self.marginal_cost_minimization(),
        ]
        current_solution_values = list(
            map(self.problem.calculate_cost_of_solution, current_solutions)
        )
        min_id = np.argmin(current_solution_values)

        best_solution = current_solutions[min_id]
        best_solution_value = current_solution_values[min_id]

        inner_iterations = self.inner_iterations
        stagnation_counter = 0

        while self.temp > 1e-4:
            improved_in_this_temp = False

            valid_evaluations = 0
            while valid_evaluations < inner_iterations:
                potential_solutions = list(map(self.find_neighbour, current_solutions))

                for id, potential_solution in enumerate(potential_solutions):
                    if potential_solution is None:
                        continue

                    valid_evaluations += 1

                    potential_solution_value = self.problem.calculate_cost_of_solution(
                        potential_solution
                    )

                    delta_e = potential_solution_value - current_solution_values[id]

                    if delta_e < 0 or random.random() < math.exp(-delta_e / self.temp):
                        current_solutions[id] = potential_solution
                        current_solution_values[id] = potential_solution_value

                        if current_solution_values[id] < best_solution_value:
                            best_solution = potential_solution
                            best_solution_value = current_solution_values[id]
                            improved_in_this_temp = True
                            stagnation_counter = 0

            self.temp *= self.alfa

            if not improved_in_this_temp:
                stagnation_counter += 1

            if stagnation_counter >= self.max_stagnation and self.reheats > 0:
                self._reheat()

                id = np.argmax(current_solution_values)

                current_solutions[id] = copy.deepcopy(best_solution)
                current_solution_values[id] = best_solution_value

                stagnation_counter = 0

        return best_solution

    def solve(self) -> Solution:
        best_solution = self._run()
        best_solution_cost = self.problem.calculate_cost_of_solution(best_solution)

        return self._polish_solution(best_solution, best_solution_cost)

    def _polish_solution(self, solution: Solution, cost: int) -> Solution:
        current_solution = copy.deepcopy(solution)
        current_solution_cost = cost

        improved = True
        while improved:
            improved = False

            neighbours = (
                [self.adjacent_swap(current_solution) for _ in range(30)]
                + [self.deadline_based_swap(current_solution) for _ in range(20)]
                + [self.swap_operator(current_solution) for _ in range(10)]
            )

            random.shuffle(neighbours)

            for neighbour in neighbours:
                if neighbour is None:
                    continue

                neighbour_cost = self.problem.calculate_cost_of_solution(neighbour)
                if neighbour_cost < current_solution_cost:
                    current_solution = neighbour
                    current_solution_cost = neighbour_cost
                    improved = True
                    break

        return current_solution

    def find_neighbour(self, solution: Solution) -> Solution | None:
        if self.temp > self.temp_initial * 0.4:
            w = [20, 50, 20, 10]
        else:
            w = [10, 5, 45, 40]

        operator = random.choices(
            population=[
                self.swap_operator,
                self.move_operator,
                self.deadline_based_swap,
                self.adjacent_swap,
            ],
            weights=w,
            k=1,
        )[0]

        return operator(solution)
