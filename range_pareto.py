import matplotlib.pyplot as plt
import numpy as np

# Data
technologies = ["Hyb_CC", "NGOxy_CC", "Hyb"]
costs = {
    "Hyb_CC": [244.61, 232.72, 220.82],
    "NGOxy_CC": [250.76, 244.39, 238.02],
    "Hyb": [261.77, 280.54, 299.31],
}
emissions = {
    "Hyb_CC": 0.14,
    "NGOxy_CC": 0.2,
    "Hyb": 0.3,
}

# Calculate average cost, min cost, and max cost for each technology
avg_costs = {tech: np.mean(cost) for tech, cost in costs.items()}
min_costs = {tech: min(cost) for tech, cost in costs.items()}
max_costs = {tech: max(cost) for tech, cost in costs.items()}

# Prepare data for plotting
x = [avg_costs[tech] for tech in technologies]  # Average costs
xerr = [
    [avg_costs[tech] - min_costs[tech] for tech in technologies],  # Lower bound
    [max_costs[tech] - avg_costs[tech] for tech in technologies],  # Upper bound
]
y = [emissions[tech] for tech in technologies]  # Emissions

# Plotting
plt.figure(figsize=(8, 6))
plt.errorbar(x, y, xerr=xerr, fmt='o', capsize=5, label="Technologies", color='b')

# Annotate points with technology names
for i, tech in enumerate(technologies):
    plt.text(x[i], y[i] + 0.01, tech, fontsize=10, ha='center')

# Customization
plt.title("Cost vs. Emissions for Technologies", fontsize=16)
plt.xlabel("Cost", fontsize=12)
plt.ylabel("Emissions", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Show plot
plt.show()
