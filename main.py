import argparse
import json
import os

from algorithm.HillClimbing import Tactic, HillClimbing
from algorithm.SimulatedAnnealing import SimulatedAnnealing
from problem.problem import Problem

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rozwiązywanie problemu job scheduling")
    parser.add_argument("-f", "--file", help="Plik, z którego wczytywane są dane")
    args = parser.parse_args()

    if not args.file:
        raise ValueError("Nie podano pliku")

    with open(os.path.join("examples", f"{args.file}.json"), "r") as file:
        data = json.load(file)

    number_of_types = data["number_of_types"]
    number_of_time_slots = data["number_of_time_slots"]
    number_of_products = data["number_of_products"]
    inventory_cost = data["inventory_cost"]
    types = data["types"]
    due_time_slots = data["due_time_slots"]
    transition_costs = data["transition_costs"]

    problem = Problem(number_of_types, number_of_time_slots, number_of_products, inventory_cost, types, due_time_slots, transition_costs)
    tactic = Tactic(0)

    hill_climbing = HillClimbing(problem, tactic, 2000, 50)
    result = hill_climbing.solve()

    print("Hill Climbing")
    print(f"Solution: {result()}")
    print(f"Cost: {problem.calculate_cost_of_solution(result)}")

    simulated_annealing = SimulatedAnnealing(problem, 500, 0.995, 25, 3, 40)
    result = simulated_annealing.solve()
    print("Simulated Annealing")
    print(f"Solution: {result()}")
    print(f"Cost: {problem.calculate_cost_of_solution(result)}")

