import json
import numpy as np
from collections import deque


def bidirectional_bfs(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    tree = data["tree"]
    states = data["states"]
    parents = data["parent"]
    goals = data["goal_nodes"]

    if not goals:
        print("No solution found")
        return []

    start = 0
    goal = int(goals[0])  # First BFS goal = shortest depth

    # Two search frontiers
    forward = deque([start])
    backward = deque([goal])

    # Node -> predecessor in each search
    visited_f = {start: None}
    visited_b = {goal: None}

    expanded_f = 0
    expanded_b = 0
    meeting = None

    if start == goal:
        meeting = start

    while forward and backward and meeting is None:

        # Expand the smaller frontier
        if len(forward) <= len(backward):

            for _ in range(len(forward)):
                node = forward.popleft()
                expanded_f += 1

                for child in tree.get(str(node), []):
                    child = int(child)

                    if child in visited_f:
                        continue

                    visited_f[child] = node
                    forward.append(child)

                    if child in visited_b:
                        meeting = child
                        break

                if meeting is not None:
                    break

        else:
            for _ in range(len(backward)):
                node = backward.popleft()
                expanded_b += 1

                # Move backwards through the stored tree
                p = parents[str(node)]

                if p is not None:
                    p = int(p)

                    if p not in visited_b:
                        visited_b[p] = node
                        backward.append(p)

                        if p in visited_f:
                            meeting = p
                            break

    if meeting is None:
        print("No solution found")
        return []

    # Reconstruct start -> meeting
    path_f = []
    node = meeting

    while node is not None:
        path_f.append(node)
        node = visited_f[node]

    path_f.reverse()

    # Reconstruct meeting -> goal
    path_b = []
    node = visited_b[meeting]

    while node is not None:
        path_b.append(node)
        node = visited_b[node]

    path = path_f + path_b

    print("\nGoal found:", goal)
    print("Meeting node:", meeting)
    print("Shortest path:", len(path) - 1, "moves")
    print("Forward expanded:", expanded_f)
    print("Backward expanded:", expanded_b)
    print("Nodes explored:", expanded_f + expanded_b)

    print("Path (node IDs):")
    print(" -> ".join(map(str, path)))

    return [
        np.array(states[str(i)], dtype=int)
        for i in path
    ]


bidirectional_bfs('trees/p1_tree.json')
bidirectional_bfs('trees/p2_tree.json')
bidirectional_bfs('trees/p3_tree.json')
bidirectional_bfs('trees/p4_tree.json')
bidirectional_bfs('trees/p5_tree.json')
bidirectional_bfs('trees/p6_tree.json')

