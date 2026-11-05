import re
import numpy as np
import matplotlib.pyplot as plt

# Read file
with open("search_stats.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Recognized solver headings
solvers = {
    "bfs search": "BFS",
    "bi directional bfs": "Bidirectional BFS",
    "dfs search": "DFS",
    "dls interative deepening": "DLS + Interative deepening"
}

results = {}
current_solver = None

# Parse data
for line in lines:
    line = line.strip()

    # Normalize headings
    heading = re.sub(r"[^a-z0-9]+", " ", line.lower()).strip()

    if heading in solvers:
        current_solver = solvers[heading]
        results.setdefault(current_solver, [])
        continue

    if current_solver is None:
        continue

    # Extract solution lengths
    match = re.search(
        r"(?:Shortest path|Path length|Solution length):\s*([\d,]+)\s*moves",
        line,
        re.IGNORECASE
    )

    if match:
        results[current_solver].append(
            int(match.group(1).replace(",", ""))
        )

    # Handle unsolved problems
    elif re.search(r"\bNo\s+(?:solution|goal)\b", line, re.IGNORECASE):
        results[current_solver].append(np.nan)

# Plot
n_problems = max(len(values) for values in results.values())
x = np.arange(1, n_problems + 1)

fig, ax = plt.subplots(figsize=(9, 5))

for solver, lengths in results.items():
    y = lengths + [np.nan] * (n_problems - len(lengths))

    ax.plot(
        x, y,
        marker="o",
        linewidth=2,
        markersize=6,
        label=solver
    )

ax.set_xticks(x)
ax.set_xticklabels([f"P{i}" for i in x])

ax.set_xlabel("Problem")
ax.set_ylabel("#Moves")
ax.set_title("Number of Moves Comparison")

ax.legend()
ax.grid(alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("solution_lengths.png", dpi=300)
plt.show()