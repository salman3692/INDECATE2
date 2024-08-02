import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output

# Step 1: Enter your file path to read the data from the CSV file into a Pandas DataFrame
file_path = r"C:\Users\msalman\Desktop\OSMOSE ETs\Python work\combinations_specific.csv"  # Replace with the actual file path
# file_path = r"C:\Users\msalman\Desktop\OSMOSE ETs\combinations parallel - 2024 - test.csv"  # Replace with the actual file path

data_df = pd.read_csv(file_path)

# Create a Dash app
app = dash.Dash(__name__)

# Add this before the app.layout definition
Technology_counts_div = html.Div(id='Technology-counts')

# Define the layout of the app
app.layout = html.Div([

    # Text Block
    html.Div([
        html.P([
            "Parallel Co-ordinate Plot to present Glass Production Decarbonisation Superstrucuture"
        ], style={'font-size': '30px','font-weight': 'bold'})
    ], style={'margin': '10px', 'text-align': 'center'}),


    # Text Block
    html.Div([
        html.P([
            "LEGEND: 1 = NG Furnace, 2 = NG Furnace with CC, , 3 = Hybrid Furnace, 4 = Hybrid Furnace with CC, 5 = Electric Furnace",
            html.Br(),
            "6 = Electric Furnace with CC, 7 = H2 Furnace, 8 = H2 Furnace with CC, 9 = NG-Oxy Furnace, 10 = NG-Oxy Furnace with CC"
        ])
    ], style={'margin': '15px', 'text-align': 'center'}),

    # Parallel Coordinates Plot
    dcc.Graph(id='parallel-coordinates-plot',
              style={'width': '100%', 'height': '500px'}),

    # Technology Dropdown
    dcc.Dropdown(
        id='Technology-dropdown',
        options=[{'label': c, 'value': c} for c in data_df['Technology'].unique()],
        value=[data_df['Technology'].unique()[0]],
        multi=True
    ),
# Input block for cEE range
html.Div([
    html.Label('cEE Range'),
    dcc.Input(
        id='cEE-min-input',
        type='number',
        value=data_df['cEE'].min(),
        style={'width': '50px'}
    ),
    dcc.Input(
        id='cEE-max-input',
        type='number',
        value=data_df['cEE'].max(),
        style={'width': '50px'}
    )
], style={'display': 'inline-block', 'margin-right': '20px', 'text-align': 'center'}),

# Input block for cH2 range
html.Div([
    html.Label('cH2 Range'),
    dcc.Input(
        id='cH2-min-input',
        type='number',
        value=data_df['cH2'].min(),
        style={'width': '50px'}
    ),
    dcc.Input(
        id='cH2-max-input',
        type='number',
        value=data_df['cH2'].max(),
        style={'width': '50px'}
    )
], style={'display': 'inline-block', 'margin-right': '20px', 'text-align': 'center'}),

# Input block for cNG range
html.Div([
    html.Label('cNG Range'),
    dcc.Input(
        id='cNG-min-input',
        type='number',
        value=data_df['cNG'].min(),
        style={'width': '50px'}
    ),
    dcc.Input(
        id='cNG-max-input',
        type='number',
        value=data_df['cNG'].max(),
        style={'width': '50px'}
    )
], style={'display': 'inline-block', 'margin-right': '20px', 'text-align': 'center'}),

# Input block for cCO2 range
html.Div([
    html.Label(['CO', html.Sub('2'), ' tax']),
    dcc.Input(
        id='cCO2-min-input',
        type='number',
        value=data_df['cCO2'].min(),
        style={'width': '50px'}
    ),
    dcc.Input(
        id='cCO2-max-input',
        type='number',
        value=data_df['cCO2'].max(),
        style={'width': '50px'}
    )
], style={'display': 'inline-block', 'margin-right': '20px', 'text-align': 'center'}),

    # Add the Technology counts div
    Technology_counts_div,
])

# Define the callback to update the plot and Technology counts
@app.callback(
    [Output('parallel-coordinates-plot', 'figure'),
     Output('Technology-counts', 'children')],
    [Input('Technology-dropdown', 'value'),
     Input('cEE-min-input', 'value'),
     Input('cEE-max-input', 'value'),
     Input('cH2-min-input', 'value'),
     Input('cH2-max-input', 'value'),
     Input('cNG-min-input', 'value'),
     Input('cNG-max-input', 'value'),
     Input('cCO2-min-input', 'value'),
     Input('cCO2-max-input', 'value')]
)
def update_parallel_coordinates_plot(selected_commodities, cEE_min, cEE_max, cH2_min, cH2_max, cNG_min, cNG_max, cCO2_min, cCO2_max):
    # Convert selected_commodities to a list if it's not already
    if not isinstance(selected_commodities, list):
        selected_commodities = [selected_commodities]

    # Filter the data based on the selected commodities and input ranges
    filtered_data = data_df[data_df['Technology'].isin(selected_commodities)]
    filtered_data = filtered_data[(filtered_data['cEE'] >= cEE_min) & (filtered_data['cEE'] <= cEE_max)]
    filtered_data = filtered_data[(filtered_data['cH2'] >= cH2_min) & (filtered_data['cH2'] <= cH2_max)]
    filtered_data = filtered_data[(filtered_data['cNG'] >= cNG_min) & (filtered_data['cNG'] <= cNG_max)]
    filtered_data = filtered_data[(filtered_data['cCO2'] >= cCO2_min) & (filtered_data['cCO2'] <= cCO2_max)]

    # Calculate the Technology counts within the selected ranges
    Technology_counts = filtered_data['Technology'].value_counts().to_dict()

    # Create the counts display as a list of HTML elements
    counts_display = []
    for Technology, count in Technology_counts.items():
        counts_display.append(html.P(f"Technology {Technology}: {count} times"))

    # Combine the counts display into a single div
    counts_div = html.Div(counts_display)

    # Create the parallel coordinates plot
    fig = go.Figure(data=
        go.Parcoords(
            line=dict(color=filtered_data['Technology'], colorscale='Blackbody'),
            dimensions=list([
                dict(range=[min(data_df['Technology']), max(data_df['Technology'])], label='Technology', values=filtered_data['Technology']),
                dict(range=[min(data_df['cEE']), max(data_df['cEE'])], label='Cost of Electricity (€/kWh)', values=filtered_data['cEE']),
                dict(range=[min(data_df['cH2']), max(data_df['cH2'])], label='Cost of Hydrogen (€/kWh)', values=filtered_data['cH2']),
                dict(range=[min(data_df['cNG']), max(data_df['cNG'])], label='Cost of Natural Gas (€/kWh)', values=filtered_data['cNG']),
                dict(range=[min(data_df['cCO2']), max(data_df['cCO2'])], label='Cost of Emissions (€/tCO2)', values=filtered_data['cCO2']),
        ]),
        unselected = dict(line = dict(color = 'green', opacity = 0.0))
        )
    )

    return fig, counts_div

# Run the app


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
