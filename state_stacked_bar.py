import re
import matplotlib.pyplot as plt
import numpy as np

# Read data
with open("tree_stats.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Parse each problem
pattern = (
    r"(p\d+)\s+tree\s+"
    r"Total tables:\s*([\d,]+)\s+"
    r"Total goals:\s*([\d,]+)"
)

matches = re.findall(pattern, text, re.IGNORECASE)

problems = []
totals = []
goals = []

for name, total, goal in matches:
    problems.append(name.upper())
    totals.append(int(total.replace(",", "")))
    goals.append(int(goal.replace(",", "")))

non_goals = np.array(totals) - np.array(goals)

# Plot
fig, ax = plt.subplots(figsize=(9, 5))

x = np.arange(len(problems))
width = 0.6

ax.bar(x, non_goals, width, label="Non-goal state", color="steelblue")
ax.bar(x, goals, width, bottom=non_goals,
       label="Goal state", color="orange")

# Total nodes above bars
for i, total in enumerate(totals):
    ax.text(x[i], total, f"{total:,}",
            ha="center", va="bottom", fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(problems)

ax.set_xlabel("Problem")
ax.set_ylabel("Number of states")
ax.set_title("Problem Search Space")
ax.legend()

ax.set_ylim(0, max(totals) * 1.15)
ax.grid(axis="y", alpha=0.25)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("problem_statistics.png", dpi=300)
plt.show()