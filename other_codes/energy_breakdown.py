import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.cm as cm
import numpy as np

# Load the data from the Excel file with the specified sheet name
file_path = 'data/energy_breakdown2.xlsx'
sheet_name = 'plot'  # Replace 'plot' with the actual sheet name in your Excel file

# If your file is a .xlsx file, specify the engine as 'openpyxl'
df = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0, engine='openpyxl')

# Transpose the DataFrame so that technologies are on the x-axis
df = df.T

# Define a colormap with a wide range of colors
colormap = cm.get_cmap('tab20', len(df.columns))

# Plotting the stacked bar chart with the new colormap
ax = df.plot(kind='bar', stacked=True, figsize=(10, 7), color=[colormap(i) for i in range(12)])

# Customizing the plot
ax.set_ylabel("Energy (Q) (MW)")
plt.xticks(rotation=45)

# Position the legend box above the plot
plt.legend(bbox_to_anchor=(0.5, 1.1), loc='center', ncol=5)

# Custom function to format y-axis labels by dividing by 1000
def thousands(x, pos):
    return f'{int(x/1000)}'

# Apply the formatter to the y-axis
ax.yaxis.set_major_formatter(FuncFormatter(thousands))

# Show the plot
plt.tight_layout()
plt.show()
