import json
import numpy as np


def dfs_search(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    tree = data["tree"]
    states = data["states"]
    goals = set(data["goal_nodes"])

    stack = [0]
    visited = {0}
    parent = {0: None}

    while stack:
        node = stack.pop()

        # Check goal
        if node in goals:
            path = []
            current = node

            while current is not None:
                path.append(current)
                current = parent[current]

            path.reverse()

            print("\nGoal found:", node)
            print("Shortest path", len(path) - 1, "moves")
            print("Nodes explored:", len(visited))

            print("Path (node IDs):")
            print(" -> ".join(map(str, path)))

            return [
                np.array(states[str(i)], dtype=int)
                for i in path
            ]

        # Explore children from saved tree
        for child in reversed(tree.get(str(node), [])):
            child = int(child)

            if child not in visited:
                visited.add(child)
                parent[child] = node
                stack.append(child)

    print("No solution found")
    return []

dfs_search('trees/p1_tree.json')
dfs_search('trees/p2_tree.json')
dfs_search('trees/p3_tree.json')
dfs_search('trees/p4_tree.json')
dfs_search('trees/p5_tree.json')
dfs_search('trees/p6_tree.json')