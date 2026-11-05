"""Build the complete first-discovery Klotski tree using NumPy board tables."""

import json
from collections import deque
from pathlib import Path

import numpy as np

from lab4_simulator import print_state, table_to_state, generate_children


def is_goal(table):
    """Target has ID 1. It must cover the bottom exit cells."""
    target_size = np.count_nonzero(table == 1)

    if target_size == 4:  # 2x2 target
        return bool(np.all(table[-1, [1, 2]] == 1))
    if target_size == 1:  # 1x1 target (p1)
        return bool(table[-1, 1] == 1)
    return False


def table_key(table):
    """A hashable representation of a numbered matrix for duplicate detection."""
    table = np.asarray(table, dtype=np.int64)
    return (table.shape, table.tobytes())


def build_tree(initial_state, save_path="klotski_tree.json"):
    """Explore every reachable distinct table with BFS, then save once.

    initial_state can be a state dictionary or a 2D NumPy table.
    Returns: tree, states, parent, status; states[node_id] is a NumPy table.
    """
    initial_table = (
        print_state(initial_state)
        if isinstance(initial_state, dict)
        else np.asarray(initial_state)
    )
    initial_table = np.asarray(initial_table, dtype=int).copy()

    tree = {0: []}
    states = {0: initial_table}
    parent = {0: None}
    status = {0: "OPEN"}
    goal_nodes = []

    visited = {table_key(initial_table)}
    pending = deque([0])
    next_id = 1

    # Keep expanding until there are no more unexplored tables.
    while pending:
        node_id = pending.popleft()
        table = states[node_id]
        if node_id % 5000 == 0:
            print(
                f"Expanded: {node_id:,} | "
                f"Discovered: {len(states):,} | "
                f"Pending: {len(pending):,}",
                flush=True
            )
        # Your simulator accepts a state dict, not a table.
        state = table_to_state(table)
        child_tables = generate_children(state)

        for child_table in child_tables:
            child_table = np.asarray(child_table, dtype=int)

            if child_table.shape != initial_table.shape:
                raise ValueError(
                    f"Child has shape {child_table.shape}, expected "
                    f"{initial_table.shape}. Do not trim the board during search."
                )

            key = table_key(child_table)
            if key in visited:
                continue

            visited.add(key)
            child_id = next_id
            next_id += 1

            states[child_id] = child_table.copy()
            tree[node_id].append(child_id)
            tree[child_id] = []
            parent[child_id] = node_id
            status[child_id] = "OPEN"
            pending.append(child_id)

        # Record goals, but continue searching until the whole tree is built.
        if is_goal(table):
            goal_nodes.append(node_id)
            status[node_id] = "GOAL"
        else:
            status[node_id] = "EXPANDED" if tree[node_id] else "END"

    # This code runs only after the BFS queue is empty.
    data = {
        "tree": tree,
        "states": {i: table.tolist() for i, table in states.items()},
        "parent": parent,
        "status": status,
        "goal_nodes": goal_nodes,
    }

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with save_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, separators=(",", ":"))

    print(f"Tree complete: {len(states)} tables saved to {save_path}")
    print(f"Goal nodes: {len(goal_nodes)}")
    return tree, states, parent, status


def load_tree(path="klotski_tree.json"):
    """Load a completed tree and restore NumPy tables + integer node IDs."""
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)

    data["tree"] = {int(k): v for k, v in data["tree"].items()}
    data["states"] = {
        int(k): np.asarray(v, dtype=int) for k, v in data["states"].items()
    }
    data["parent"] = {int(k): v for k, v in data["parent"].items()}
    data["status"] = {int(k): v for k, v in data["status"].items()}
    return data


def solution_path(parent, goal_node):
    """Return node IDs from initial table to the chosen goal node."""
    path = []
    while goal_node is not None:
        path.append(goal_node)
        goal_node = parent[goal_node]
    return path[::-1]


if __name__ == "__main__":
    from lab4_states import p3

    tree, states, parent, status = build_tree(p3, "p3_tree.json")
