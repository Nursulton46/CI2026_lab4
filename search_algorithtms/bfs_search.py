import json
import numpy as np
from collections import deque


def bfs_search(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    tree = data["tree"]
    states = data["states"]
    goals = set(data["goal_nodes"])

    queue = deque([0])
    visited = {0}
    parent = {0: None}

    while queue:
        node = queue.popleft()

        # Check goal
        if node in goals:
            path = []
            current = node

            while current is not None:
                path.append(current)
                current = parent[current]

            path.reverse()

            print("\n\nGoal found:", node)
            print("Shortest path:", len(path) - 1, "moves")
            print("Nodes explored:", len(visited))

            print("Path (node IDs):")
            print(" -> ".join(map(str, path)))

            return [
                np.array(states[str(i)], dtype=int)
                for i in path
            ]

        # Explore children from saved tree
        for child in tree.get(str(node), []):
            child = int(child)

            if child not in visited:
                visited.add(child)
                parent[child] = node
                queue.append(child)

    print("No solution found")
    return []

bfs_search('trees/p1_tree.json')
bfs_search('trees/p2_tree.json')
bfs_search('trees/p3_tree.json')
bfs_search('trees/p4_tree.json')
bfs_search('trees/p5_tree.json')
bfs_search('trees/p6_tree.json')
