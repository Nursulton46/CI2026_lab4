"""Explore a Klotski tree saved by lab4_tree_builder.py.

Usage:
    python play_tree.py p3_tree.json

This is a viewer of the BFS first-discovery tree, not a game engine:
child choices are newly discovered states, not necessarily every legal move.
"""

import json
import sys
from pathlib import Path
import numpy as np


def load_data(path):
    # Keep tables as nested Python lists in memory. Converting millions of
    # tables to individual NumPy arrays would consume extra RAM.
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)
    for field in ("tree", "states", "parent", "status"):
        if field not in data:
            raise ValueError(f"Missing '{field}' in JSON")
    return data


def board(data, node_id):
    return np.asarray(data["states"][str(node_id)], dtype=int)


def ancestor_path(data, node_id):
    path = []
    while node_id is not None:
        path.append(node_id)
        node_id = data["parent"].get(str(node_id))
    return path[::-1]


def show_node(data, node_id):
    node = str(node_id)
    if node not in data["states"]:
        print(f"Unknown node ID: {node_id}")
        return
    table = board(data, node_id)
    children = data["tree"].get(node, [])
    depth = len(ancestor_path(data, node_id)) - 1
    print(f"\nNode {node_id} | layer {depth} | {data['status'].get(node, '?')} | "
          f"{len(children)} tree children")
    print(table)
    if children:
        print("Type 'n' to see children, then type a child index to move there.")


def show_children(data, node_id):
    children = data["tree"].get(str(node_id), [])
    if not children:
        print("No children in the stored tree.")
    for index, child_id in enumerate(children):
        print(f"\n[{index}] node {child_id} ({data['status'].get(str(child_id), '?')})")
        print(board(data, child_id))


def show_help():
    print("""
Commands:
  n             display all child tables with their indices
  0, 1, ...     choose a child by its index
  b             back to parent
  r             return to root (node 0)
  goto ID       jump to a node ID
  goals         list first 20 goal node IDs (and total)
  goal          jump to the first goal node
  path          show node IDs on path from root to current node
  replay        print all tables along that path
  stats         show counts and statuses
  h             help
  q             quit
""")


def play(data):
    current = 0
    goal_nodes = data.get("goal_nodes", [])
    print(f"Loaded {len(data['states']):,} tables and {len(goal_nodes):,} goal nodes.")
    show_help()
    show_node(data, current)

    while True:
        try:
            command = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return

        if command in ("q", "quit", "exit"):
            break
        elif command in ("h", "help", "?"):
            show_help()
            continue
        elif command in ("n", "children"):
            show_children(data, current)
            continue
        elif command in ("b", "back", "p"):
            parent = data["parent"].get(str(current))
            if parent is None:
                print("Already at root.")
                continue
            current = parent
        elif command in ("r", "root"):
            current = 0
        elif command in ("goals",):
            print(f"Total goal nodes: {len(goal_nodes):,}")
            print("First 20:", goal_nodes[:20])
            continue
        elif command == "goal":
            if not goal_nodes:
                print("No goal nodes recorded.")
                continue
            current = goal_nodes[0]
        elif command in ("path", "replay"):
            path = ancestor_path(data, current)
            print(f"Path length: {len(path) - 1} moves")
            print(" -> ".join(map(str, path)))
            if command == "replay":
                for step, node_id in enumerate(path):
                    print(f"\nStep {step}, node {node_id}")
                    print(board(data, node_id))
            continue
        elif command == "stats":
            print(f"Total tables: {len(data['states']):,}")
            print(f"Total goals: {len(goal_nodes):,}")
            print(f"Recorded nodes: {len(data['tree']):,}")
            continue
        elif command.startswith("goto "):
            node_str = command[5:].strip()
            if not node_str.isdecimal() or node_str not in data["states"]:
                print("Unknown node ID.")
                continue
            current = int(node_str)
        elif command.isdecimal():
            choices = data["tree"].get(str(current), [])
            index = int(command)
            if index >= len(choices):
                print(f"Invalid child index. Choose 0..{len(choices) - 1}.")
                continue
            current = choices[index]
        else:
            print("Unknown command. Type h for help.")
            continue

        show_node(data, current)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "p5_tree.json"
    print(f"Loading {path} ...", flush=True)
    try:
        data = load_data(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Cannot load tree: {error}")
        sys.exit(1)
    play(data)




if __name__ == "__main__":
    main()

