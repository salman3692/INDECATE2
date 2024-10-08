import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Defining the technologies on the x-axis
technologies = ['NG', 'NG_CC', 'NGOxy', 'NGOxy_CC', 'Hyb', 'Hyb_CC', 'EL', 'EL_CC', 'H2', 'H2_CC']

# Energy data for each technology (same as before)
qth_furnace = [5.80, 5.80, 4.72, 4.72, 1.99, 1.99, 0, 0, 5.94, 5.94]
qel_furnace = [0.80, 0.80, 0.80, 0.80, 2.23, 2.23, 3.73, 3.73, 0.80, 0.80]
qth_ccu = [0, 1.49, 0, 1.99, 0, 2.23, 0, 3.73, 0, 5.94]  # Example dummy data
qel_ccu = [0, 0.27, 0, 0.54, 0, 0.36, 0, 0.23, 0, 0.09]
qel_cpu = [0, 0, 0.32, 0.32, 0.13, 0.13, 0, 0, 0, 0]
qth_boiler = [0.81, 0.81, 0, 0, 0, 0, 0, 0, 0, 0]
qel_whr = [-0.28, -0.68, -0.34, -0.34, -0.19, -0.19, 0, 0, -0.31, -0.51]
emissions_impact = [0.63, 0.20, 0.55, 0.36, 0.12, 0.08, 0, 0, 0.27, 0.10]

# Create the figure
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add each energy category as a stacked bar (all visible by default)
bars = []
bars.append(go.Bar(name='Qth-Furnace', x=technologies, y=qth_furnace, marker_color='red', visible=True))
bars.append(go.Bar(name='Qel-Furnace', x=technologies, y=qel_furnace, marker_color='gray', visible=True))
bars.append(go.Bar(name='Qth-CCU', x=technologies, y=qth_ccu, marker_color='black', visible=True))
bars.append(go.Bar(name='Qel-CCU', x=technologies, y=qel_ccu, marker_color='yellow', visible=True))
bars.append(go.Bar(name='Qel-CPU', x=technologies, y=qel_cpu, marker_color='green', visible=True))
bars.append(go.Bar(name='Qth-Boiler', x=technologies, y=qth_boiler, marker_color='brown', visible=True))
bars.append(go.Bar(name='Qel-WHR', x=technologies, y=qel_whr, marker_color='blue', visible=True))

# Adding emissions as separate markers
scatter = go.Scatter(name='Emissions Impact', x=technologies, y=emissions_impact, mode='markers',
                     marker=dict(color='black', size=10), yaxis='y2', visible=True)

# Add all traces to the figure
for trace in bars:
    fig.add_trace(trace)
fig.add_trace(scatter)

# Update layout for stacked bars and dual y-axis
fig.update_layout(
    barmode='stack',
    title='Interactive Energy Breakdown and Emissions Impact',
    xaxis=dict(title='Technologies'),
    yaxis=dict(title='Energy Consumption (GJ/t Glass)'),
    yaxis2=dict(title='Specific Emissions (TCO2/T Glass)', overlaying='y', side='right'),
    height=600,
    updatemenus=[
        dict(
            buttons=[
                dict(label="All Technologies",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},  # Show all bars and scatter
                           {"title": "All Technologies"}]),
                dict(label="NG",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "NG only"}]),
                dict(label="NG_CC",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "NG_CC only"}]),
                dict(label="NGOxy",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "NGOxy only"}]),
                dict(label="NGOxy_CC",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "NGOxy_CC only"}]),
                dict(label="Hyb",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "Hyb only"}]),
                dict(label="Hyb_CC",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "Hyb_CC only"}]),
                dict(label="EL",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "EL only"}]),
                dict(label="EL_CC",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "EL_CC only"}]),
                dict(label="H2",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "H2 only"}]),
                dict(label="H2_CC",
                     method="update",
                     args=[{"visible": [True] * (len(bars) + 1)},
                           {"title": "H2_CC only"}])
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.17,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
    ]
)

# Show the plot
fig.show()
