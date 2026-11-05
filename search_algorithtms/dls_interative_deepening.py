import json
import numpy as np


def dls(tree, goals, limit, start=0):
    stack = [(start, 0)]
    expanded = 0
    cutoff = False

    while stack:
        node, depth = stack.pop()
        expanded += 1

        # Goal check
        if node in goals:
            return node, expanded, cutoff

        # Depth limit reached
        if depth >= limit:
            if tree.get(str(node), []):
                cutoff = True
            continue

        # DFS: visit children in their stored order
        children = tree.get(str(node), [])

        for child in reversed(children):
            stack.append((int(child), depth + 1))

    return None, expanded, cutoff


def iterative_deepening(json_path, K=0, max_depth=None):
    with open(json_path, "r") as f:
        data = json.load(f)

    tree = data["tree"]
    states = data["states"]
    parent = data["parent"]
    goals = set(map(int, data["goal_nodes"]))

    depth = K
    total_expanded = 0

    while max_depth is None or depth <= max_depth:

        goal, expanded, cutoff = dls(
            tree, goals, limit=depth
        )

        total_expanded += expanded


        if goal is not None:
            path = []
            node = goal

            while node is not None:
                path.append(node)
                node = parent[str(node)]
                if node is not None:
                    node = int(node)

            path.reverse()

            print("\nGoal found:", goal)
            print("Shortest path", len(path) - 1, "moves")
            print("Nodes explored:", total_expanded)

            print("Path (node IDs):")
            print(" -> ".join(map(str, path)))

            return [
                np.array(states[str(i)], dtype=int)
                for i in path
            ]

        if not cutoff:
            print("No solution found")
            return []

        depth += 1

    print("No solution found")
    return []

iterative_deepening('trees/p1_tree.json', 80)
iterative_deepening('trees/p2_tree.json', 80)
iterative_deepening('trees/p3_tree.json', 80)
iterative_deepening('trees/p4_tree.json', 80)
iterative_deepening('trees/p5_tree.json', 80)
iterative_deepening('trees/p6_tree.json', 80)