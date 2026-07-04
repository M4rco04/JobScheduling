import copy

from problem.solution import Solution


class Problem:
    def __init__(
        self,
        number_of_types: int,
        number_of_slots: int,
        products: int,
        inventory_cost: int,
        types: list[int],
        due_time_slots: list[int],
        transition_costs: list[list[int]],
    ):
        self.number_of_types: int = number_of_types
        self.number_of_slots: int = number_of_slots
        self.products: int = products
        self.inventory_cost: int = inventory_cost
        self.types: list[int] = types.copy()
        self.due_time_slots: list[int] = due_time_slots.copy()
        self.transition_costs: list[list[int]] = copy.deepcopy(transition_costs)

    def calculate_cost_of_solution(self, solution: Solution) -> int:
        return self._calculate_transition_costs(
            solution()
        ) + self._calculate_inventory_costs(solution())

    def _calculate_transition_costs(self, solution: list[int | None]) -> int:
        cost: int = 0

        last_product: int | None = solution[0]
        for id in range(1, len(solution)):
            if solution[id] is None:
                continue

            if last_product is None:
                last_product = solution[id]
                continue

            last_product_type: int = self.types[last_product]
            actual_product_type: int = self.types[solution[id]]

            cost += self.transition_costs[last_product_type][actual_product_type]
            last_product = solution[id]

        return cost

    def _calculate_inventory_costs(self, solution: list[int | None]) -> int:
        cost: int = 0

        for id in range(0, len(solution)):
            if solution[id] is None:
                continue

            product_id: int = solution[id]
            delta = self.due_time_slots[product_id] - id

            cost += self.inventory_cost * delta

        return cost

    def is_solution_valid(self, solution: Solution) -> bool:
        positions = {}

        for slot, product in enumerate(solution()):
            if product is not None:
                positions[product] = slot

        for product, deadline in enumerate(self.due_time_slots):
            if product not in positions:
                return False

            if positions[product] > deadline:
                return False

        return True
