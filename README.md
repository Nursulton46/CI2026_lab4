# Computational Intelligence — Lab 4

Comparison of uninformed search algorithms for solving the Klotski sliding-block puzzle.

## Implemented Algorithms

- Breadth-First Search (BFS)
- Bidirectional BFS
- Depth-First Search (DFS)
- Depth-Limited Search with Iterative Deepening (IDDFS)

## Results — Solution Length (Moves)

| Solver | P1 | P2 | P3 | P4 | P5 | P6 |
|---|---:|---:|---:|---:|---:|---:|
| BFS | 8 | 18 | 45 | 116 | 179 | — |
| Bi-BFS | 8 | 18 | 45 | 116 | 179 | — |
| DFS | 9 | 18 | 45 | 118 | 187 | — |
| IDDFS | 9 | 18 | 45 | 116 | 179 | — |

P6 has no reachable goal state.

## Report

[Computational Intelligence Lab 4 Report](comp_intel_lab4.pdf)

## Experimental Data

- `p1_tree.json` – `p6_tree.json`: Problem trees
- `tree_stats.txt`: Tree statistics
- `search_stats.txt`: Algorithm results
- PNG files: Experimental visualizations

## Implementation

The repository contains Python scripts for tree generation, search algorithms, verification, and visualization.
