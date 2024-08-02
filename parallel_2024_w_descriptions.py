import pandas as pd
import plotly.graph_objects as go
import dash
import os
from dash import dcc, html, Input, Output
import NG_furnace as ng_fired
# import ng_oxyfuel_description as ng_oxyfuel

# Step 1: Enter your file path to read the data from the CSV file into a Pandas DataFrame
file_path = os.getenv('file_path', 'combinations_specific4.csv')

data_df = pd.read_csv(file_path)

# Map TRL text values to numerical values
TRL_mapping = {
    'Low: 3 - 4': 1,
    'Medium: 6 - 7': 2,
    'High: 8': 3,
    'High: 9': 4
}
data_df['TRL_num'] = data_df['TRL'].map(TRL_mapping)

# Create a Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Create a function to generate the main page layout
def main_layout():
    return html.Div([

        # Text Block
        html.Div([
            html.P([
                "Parallel Co-ordinate Plot to present Glass Production Decarbonisation Superstrucuture"
            ], style={'font-size': '30px', 'font-weight': 'bold'})
        ], style={'margin': '10px', 'text-align': 'center'}),

        html.Div([
            html.P([
                html.B("List of Technologies: "),
                dcc.Link("NG-fired Furnace", href='/ng-fired'),
                ", ",
                dcc.Link("NG-Oxyfuel Furnace", href='/ng-oxyfuel'),
                ", ",
                dcc.Link("Hybrid Furnace (Electric boosting)", href='/hybrid'),
                ", ",
                dcc.Link("All Electric Furnace", href='/all-electric'),
                ", ",
                dcc.Link(["H", html.Sub("2"), "-fired Furnace"], href='/h2-fired')
            ]),
            html.Br(),
            html.I("Carbon Capture and Heat Recovery is included in all technologies")
        ], style={'margin': '1px', 'text-align': 'center'}),

        # Parallel Coordinates Plot
        dcc.Graph(id='parallel-coordinates-plot',
                  style={'width': '100%', 'height': '525px'}),

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
        html.Div(id='Technology-counts')
    ])

# Create a function to generate the description page layout
def description_layout(title, description):
    return html.Div([
        dcc.Link('Back to main page', href='/'),
        html.H2(title),
        html.P(description)
    ])

# Define the callback to update the page content based on the URL
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/ng-fired':
        return ng_fired.description_layout()
    elif pathname == '/ng-oxyfuel':
        return description_layout("NG-Oxyfuel Furnace", "NG-Oxyfuel furnaces use a combination of natural gas and pure oxygen to achieve higher combustion temperatures and improve efficiency. This technology can reduce the volume of flue gas and lower emissions.")
    elif pathname == '/hybrid':
        return description_layout("Hybrid Furnace (Electric boosting)", "Hybrid furnaces combine traditional fuel sources like natural gas with electric boosting to achieve higher temperatures and improve energy efficiency. This approach can reduce CO2 emissions and improve control over the glass melting process.")
    elif pathname == '/all-electric':
        return description_layout("All Electric Furnace", "All electric furnaces rely entirely on electricity to melt the glass. These furnaces are capable of achieving high temperatures with precise control, making them suitable for high-quality glass production. They also eliminate direct CO2 emissions associated with combustion processes.")
    elif pathname == '/h2-fired':
        return description_layout("H2-fired Furnace", "H2-fired furnaces use hydrogen as a fuel source, offering a carbon-free alternative to traditional fossil fuels. Hydrogen combustion produces water vapor as the only by-product, making it a promising option for reducing greenhouse gas emissions in the glass industry.")
    else:
        return main_layout()

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
                dict(range=[1, 5], tickvals=[1, 2, 3, 4, 5], ticktext=['NG-fired', 'NG-Oxyfuel', 'Hybrid', 'All-Electric', 'H2-fired'], label='<b>Technology</b>', values=filtered_data['Technology']),
                dict(range=[data_df['cEE'].min(), data_df['cEE'].max()], tickvals=[0.001, 0.01, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2], label='Cost of Electricity (€/kWh)', values=filtered_data['cEE']),
                dict(range=[data_df['cH2'].min(), data_df['cH2'].max()], tickvals=[0.001, 0.01, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2], label='Cost of Hydrogen (€/kWh)', values=filtered_data['cH2']),
                dict(range=[data_df['cNG'].min(), data_df['cNG'].max()], tickvals=[0.01, 0.035, 0.075, 0.1], label='Cost of Natural Gas (€/kWh)', values=filtered_data['cNG']),
                dict(range=[data_df['cCO2'].min(), data_df['cCO2'].max()], tickvals =[80, 150, 250, 350], label='Cost of Emissions (€/tCO2)', values=filtered_data['cCO2']),
                dict(range=[data_df['EI'].min(), data_df['EI'].max()], tickvals=data_df['EI'].unique(), label='Emissions Impact: tCO2/tglass', values=filtered_data['EI']),
                dict(range=[1, 4], tickvals=[1, 2, 3, 4], ticktext=['Low: 3 - 4', 'Medium: 6 - 7', 'High: 8', 'High: 9'], label='TRL', values=filtered_data['TRL_num'])
            ])
        )
    )

    return fig, counts_div

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
