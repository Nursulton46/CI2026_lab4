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
    "dls interative deepening": "DLS + Interative deepening",
    "dls iterative deepening": "DLS + Interative deepening",
    "iddfs": "DLS + Interative deepening",
}

results = {}
current_solver = None

# Parse data
for line in lines:
    line = line.strip()

    heading = re.sub(r"[^a-z0-9]+", " ", line.lower()).strip()

    if heading in solvers:
        current_solver = solvers[heading]
        results.setdefault(current_solver, [])
        continue

    if current_solver is None:
        continue

    # Read exploration count
    match = re.search(
        r"(?:Nodes explored|Total expanded):\s*([\d,]+)",
        line,
        re.IGNORECASE
    )

    if match:
        results[current_solver].append(
            int(match.group(1).replace(",", ""))
        )

    # Do NOT append NaN when "No solution found" appears

# Print extracted data
print("\n========== EXTRACTED DATA ==========")
for solver, values in results.items():
    print(f"\n{solver} ({len(values)} problems):")
    for i, val in enumerate(values, start=1):
        if np.isnan(val):
            print(f"  P{i}: No solution")
        else:
            print(f"  P{i}: {int(val)} nodes")

# Print comparison table
print("\n========== COMPARISON TABLE ==========")
n_problems = max(len(v) for v in results.values())

print(f"{'Problem':<10}", end="")
for solver in results:
    print(f"{solver:<28}", end="")
print()

for i in range(n_problems):
    print(f"{'P'+str(i+1):<10}", end="")
    for solver, values in results.items():
        if i >= len(values) or np.isnan(values[i]):
            value = "N/A"
        else:
            value = f"{int(values[i]):,}"
        print(f"{value:<28}", end="")
    print()

# Validation
print("\n========== VALIDATION ==========")
for solver, values in results.items():
    if len(values) != n_problems:
        print(f"WARNING: {solver} has only {len(values)} / {n_problems} results")
    else:
        print(f"OK: {solver} has {len(values)} results")

# Plot
x = np.arange(1, n_problems + 1)

fig, ax = plt.subplots(figsize=(9, 5))

for solver, values in results.items():
    y = values + [np.nan] * (n_problems - len(values))
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
ax.set_ylabel("States explored (log scale)")
ax.set_title("Search Cost")
ax.set_yscale("log")

ax.legend()
ax.grid(alpha=0.3, which="both")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("nodes_explored_comparison.png", dpi=300)
plt.show()
