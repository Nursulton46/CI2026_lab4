import numpy as np
from lab4_simulator import table_to_state, generate_children
from lab4_tree_builder import load_tree, solution_path

# Load saved tree
data = load_tree("p5_tree.json")

states = data["states"]
parent = data["parent"]

# First goal node
goal_id = data["goal_nodes"][0]

# Reconstruct solution path
path = solution_path(parent, goal_id)

print(f"Verifying {len(path) - 1} moves...")

for a, b in zip(path[:-1], path[1:]):
    parent_table = np.array(states[a], dtype=int)
    child_table = np.array(states[b], dtype=int)

    generated = generate_children(
        table_to_state(parent_table)
    )

    assert any(
        np.array_equal(child_table, candidate)
        for candidate in generated
    ), f"Invalid transition: {a} -> {b}"

print("All moves verified successfully!")