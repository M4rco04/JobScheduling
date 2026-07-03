from abc import ABC, abstractmethod
from enum import Enum
import random

from problem.problem import Problem
from problem.solution import Solution

class Tactic(Enum):
    BestImproving = 0
    FirstImproving = 1

class Algorithm(ABC):
    def __init__(self, problem: Problem):
        self.problem = problem

    @abstractmethod
    def solve(self) -> Solution:
        pass

    def backward_greedy(self) -> Solution:
        solution = [None] * self.problem.number_of_slots

        products = sorted(
            range(self.problem.products),
            key=lambda p: self.problem.due_time_slots[p]
        )

        for product in products:
            deadline = self.problem.due_time_slots[product]

            for slot in range(deadline, -1, -1):
                if solution[slot] is None:
                    solution[slot] = product
                    break
            else:
                raise ValueError("No feasible schedule")

        return Solution(solution)

    def greedy_type_grouping(self) -> Solution:
        solution = [None] * self.problem.number_of_slots
        unscheduled = set(range(self.problem.products))

        def is_feasible(jobs_to_check: set, start_slot: int) -> bool:
            sorted_check = sorted(list(jobs_to_check), key=lambda x: self.problem.due_time_slots[x])
            for i, j in enumerate(sorted_check):
                if start_slot + i > self.problem.due_time_slots[j]:
                    return False
            return True

        for current_slot in range(self.problem.number_of_slots):
            if not unscheduled:
                break

            prev_type = None
            if current_slot > 0 and solution[current_slot - 1] is not None:
                prev_type = self.problem.types[solution[current_slot - 1]]

            sorted_jobs = sorted(list(unscheduled), key=lambda x: self.problem.due_time_slots[x])
            chosen_job = None

            if prev_type is not None:
                same_type_jobs = [j for j in sorted_jobs if self.problem.types[j] == prev_type]
                for candidate in same_type_jobs:
                    remaining = unscheduled - {candidate}
                    if is_feasible(remaining, current_slot + 1):
                        chosen_job = candidate
                        break

            if chosen_job is None:
                for candidate in sorted_jobs:
                    remaining = unscheduled - {candidate}
                    if is_feasible(remaining, current_slot + 1):
                        chosen_job = candidate
                        break

            if chosen_job is None:
                raise ValueError(f"No feasible schedule.")

            solution[current_slot] = chosen_job
            unscheduled.remove(chosen_job)

        return Solution(solution)


    def marginal_cost_minimization(self) -> Solution:
        solution = [None] * self.problem.number_of_slots
        unscheduled_jobs = set(range(self.problem.products))

        for current_slot in range(self.problem.number_of_slots):
            if not unscheduled_jobs:
                break

            best_job = None
            best_marginal_cost = float('inf')

            prev_type = None
            for s in range(current_slot - 1, -1, -1):
                if solution[s] is not None:
                    prev_type = self.problem.types[solution[s]]
                    break

            sorted_candidates = sorted(list(unscheduled_jobs), key=lambda j: self.problem.due_time_slots[j])

            most_urgent_job = sorted_candidates[0]
            most_urgent_slack = self.problem.due_time_slots[most_urgent_job] - current_slot

            if most_urgent_slack <= 0:
                candidates = [j for j in sorted_candidates if self.problem.due_time_slots[j] - current_slot <= 0]
            else:
                candidates = sorted_candidates

            for job in candidates:
                deadline = self.problem.due_time_slots[job]

                if current_slot > deadline:
                    raise ValueError("No feasible schedule.")

                earliness = deadline - current_slot
                earliness_cost = earliness * self.problem.inventory_cost

                job_type = self.problem.types[job]
                switching_cost = 0

                if prev_type is not None:
                    switching_cost = self.problem.transition_costs[prev_type][job_type]

                total_cost = earliness_cost + switching_cost

                if total_cost < best_marginal_cost:
                    best_marginal_cost = total_cost
                    best_job = job

            if best_job is not None:
                solution[current_slot] = best_job
                unscheduled_jobs.remove(best_job)

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

    def deadline_based_swap(self, solution):
        tmp = solution().copy()
        all_indices = range(len(tmp))

        if len(tmp) < 2:
            return None

        def slack(i, job_id):
            if job_id is None:
                return float("inf")
            deadline = self.problem.due_time_slots[job_id]
            return deadline - i

        early_indices = [i for i in all_indices if tmp[i] is not None and slack(i, tmp[i]) > 0]

        if not early_indices:
            a, b = random.sample(all_indices, 2)
        else:
            a = random.choice(early_indices)

            max_index = self.problem.due_time_slots[tmp[a]]
            valid_targets = [i for i in all_indices if a < i <= max_index]

            if not valid_targets:
                b = random.choice([i for i in all_indices if i != a])
            else:
                b = random.choice(valid_targets)

        tmp[a], tmp[b] = tmp[b], tmp[a]

        new_solution = Solution(tmp)
        return new_solution if self.problem.is_solution_valid(new_solution) else None


    def adjacent_swap(self, solution: Solution) -> Solution | None:
        tmp_solution = solution().copy()

        indices = [i for i, x in enumerate(tmp_solution) if x is not None]
        a = random.choice(indices)

        possible_neighbors = []
        if a > 0:
            possible_neighbors.append(a - 1)
        if a < len(tmp_solution) - 1:
            possible_neighbors.append(a + 1)

        b = random.choice(possible_neighbors)
        tmp_solution[a], tmp_solution[b] = tmp_solution[b], tmp_solution[a]

        new_solution = Solution(tmp_solution)
        return new_solution if self.problem.is_solution_valid(new_solution) else None