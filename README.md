# 🏭 Single Machine Job Scheduling Optimizer

A Python-based optimization tool for solving a **single-machine job scheduling problem** with **hard deadlines** and **sequence-dependent setup costs**.

The optimizer schedules a set of products (jobs) into discrete time slots while ensuring that every job is completed before its deadline and minimizing the overall production cost.

---

# 📖 Problem Description

The scheduling problem consists of assigning products to a single production machine over a fixed number of time slots.

Each product:

- belongs to a specific **product type**,
- must be completed **no later than its deadline**,
- occupies exactly one time slot.

The objective is to minimize the total production cost while maintaining a feasible schedule.

## 💰 Cost Function

The total cost consists of two components:

### 📦 Inventory Cost (Earliness Penalty)

Completing a product before its deadline generates inventory holding costs.

- Finishing exactly at the deadline results in zero inventory cost.
- The earlier a product is completed, the larger the penalty.

### 🔄 Transition Cost (Sequence-Dependent Setup Cost)

Changing production from one product type to another incurs a setup cost.

The transition cost depends on the order of consecutive product types and is defined by a transition cost matrix provided in the input instance.

---

# 📋 Constraints

A schedule is considered **feasible** if:

- ✅ every product is scheduled exactly once,
- ✅ no two products occupy the same time slot,
- ✅ every product finishes on or before its deadline.

---

# 🚀 Optimization Approach

The optimizer combines fast constructive heuristics with metaheuristic optimization algorithms.

## 🏗️ 1. Constructive Heuristics

To provide high-quality initial solutions, one of the following heuristics is selected randomly.

### ⏪ Backward Greedy

Builds the schedule backwards from the latest time slots.

Jobs are assigned as close as possible to their deadlines, guaranteeing a feasible initial schedule.

### 🧩 Greedy Type Grouping

Attempts to schedule products of the same type consecutively to reduce transition costs while maintaining feasibility.

### 🎯 Marginal Cost Minimization

Constructs the schedule slot by slot.

For each position, the heuristic selects the feasible job with the lowest estimated increase in total cost (inventory cost + transition cost).

---

## 🧠 2. Metaheuristics

### ⛰️ Hill Climbing

A local search algorithm that iteratively improves the current solution by exploring neighboring schedules.

Supported strategies:

- **Best Improving** – evaluates all neighboring solutions and chooses the best improvement.
- **First Improving** – accepts the first improving neighbor found.

Additional features:

- restart mechanism,
- freeze threshold to escape local optima.

---

### 🔥 Simulated Annealing

A probabilistic optimization algorithm capable of escaping local minima by occasionally accepting worse solutions.

Key features include:

- temperature-based acceptance criterion,
- dynamic operator weighting,
- reheating mechanism after prolonged stagnation,
- final local search ("polishing") phase to reach a local optimum.

---

# 🔧 Neighborhood Operators

The search algorithms generate neighboring solutions using several mutation operators.

### Swap

Randomly exchanges the positions of two jobs.

### Move

Removes a job from its current position and inserts it into another valid position.

### Deadline-Based Swap

Swaps a job with positive slack (completed well before its deadline) with another job scheduled closer to its deadline.

### Adjacent Swap

Swaps two consecutive jobs.

---

# 📂 Project Structure

| File | Description |
|------|-------------|
| `main.py` | Entry point of the application. Parses CLI arguments, loads JSON instances, and executes the optimization algorithms. |
| `problem/problem.py` | Defines the scheduling problem, cost function, and feasibility constraints. |
| `problem/solution.py` | Represents a schedule and provides utility methods for solution handling. |
| `algorithm/Algorithm.py` | Abstract base class containing constructive heuristics and neighborhood operators. |
| `algorithm/HillClimbing.py` | Hill Climbing implementation. |
| `algorithm/SimulatedAnnealing.py` | Simulated Annealing implementation with reheating and final polishing. |
| `examples/*.json` | Example problem instances. |

---

# 📥 Input Format

Problem instances are provided as JSON files located in the `examples/` directory.

Each instance contains:

- 🕒 number of time slots,
- 📦 product types,
- ⏰ product deadlines,
- 🔄 transition cost matrix,
- ⚙️ additional problem-specific parameters.

---

# ⚙️ Requirements

- 🐍 Python **3.10+**
- 🔢 NumPy

Install dependencies:

```bash
pip install numpy
```

---

# ▶️ Running the Optimizer

Run the optimizer by specifying the dataset name.

```bash
python main.py -f 04
```

For example, the command above loads:

```text
examples/04.json
```

---

# 📊 Output

For each optimization algorithm, the program reports:

- 📅 the final production schedule,
- 💰 the minimized total cost.

Example:

```text
Hill Climbing
Solution: [1, 0, 4, 3, 5, None, 6, None, 2, None]
Cost: 761
Simulated Annealing
Solution: [None, 0, 5, 1, 4, 3, 6, None, 2, None]
Cost: 763
```

---

# 🛠️ Implemented Algorithms

## 🏗️ Constructive Heuristics

- Backward Greedy
- Greedy Type Grouping
- Marginal Cost Minimization

## 🧠 Metaheuristics

- ⛰️ Hill Climbing
  - Best Improving
  - First Improving
- 🔥 Simulated Annealing

## 🔧 Neighborhood Operators

- Swap
- Move
- Deadline-Based Swap
- Adjacent Swap
