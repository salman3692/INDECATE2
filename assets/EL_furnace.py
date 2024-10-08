import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_interactions import interactive_plot
from matplotlib.lines import Line2D

# Sample DataFrame
np.random.seed(0)
n = 100
data_df = pd.DataFrame({
    'Technology': np.random.choice(['NG-fired', 'NG-Oxyfuel', 'Hybrid', 'All-Electric', 'H2-fired'], n),
    'cEE': np.random.rand(n),
    'cH2': np.random.rand(n),
    'cNG': np.random.rand(n),
    'cCO2': np.random.rand(n),
    'EI': np.random.rand(n) * 100,
    'TRL': np.random.choice(['Low: 3 - 4', 'Medium: 6 - 7', 'High: 8', 'High: 9'], n)
})

# Encode categorical variables
technology_mapping = {
    'NG-fired': 1,
    'NG-Oxyfuel': 2,
    'Hybrid': 3,
    'All-Electric': 4,
    'H2-fired': 5
}
TRL_mapping = {
    'Low: 3 - 4': 1,
    'Medium: 6 - 7': 2,
    'High: 8': 3,
    'High: 9': 4
}
data_df['Technology_num'] = data_df['Technology'].map(technology_mapping)
data_df['TRL_num'] = data_df['TRL'].map(TRL_mapping)

# Function to plot parallel coordinates
def plot_parallel_coordinates(selected_techs):
    plt.figure(figsize=(12, 8))
    colors = {'NG-fired': 'blue', 'NG-Oxyfuel': 'green', 'Hybrid': 'red', 'All-Electric': 'orange', 'H2-fired': 'purple'}
    
    # Filter the data based on selected technologies
    filtered_df = data_df[data_df['Technology'].isin(selected_techs)]

    # Create parallel coordinates plot
    for tech in selected_techs:
        tech_data = filtered_df[filtered_df['Technology'] == tech]
        plt.plot(tech_data[['cEE', 'cH2', 'cNG', 'cCO2', 'EI']].values.T, 
                 color=colors[tech], alpha=0.5, label=tech)

    # Adding labels
    plt.xticks(ticks=range(5), labels=['cEE', 'cH2', 'cNG', 'cCO2', 'EI'])
    plt.xlabel('Features')
    plt.ylabel('Values')
    plt.title('Parallel Coordinates Plot')
    plt.legend()
    plt.grid(True)
    plt.show()

# Interactive plotting
def interactive_parallel_coordinates():
    technologies = data_df['Technology'].unique()
    interactive_plot(
        plot_parallel_coordinates,
        selected_techs=technologies,
        dropdown_options=technologies,
        title='Select Technologies to Display'
    )

# Run interactive plot
interactive_parallel_coordinates()
