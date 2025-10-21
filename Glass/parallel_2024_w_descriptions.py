import pandas as pd
import plotly.graph_objects as go
import dash
import os
from dash import dcc, html, Input, Output
import ng_furnace as ng_fired

# Enter your file path to read the data from the CSV file into a Pandas DataFrame
file_path = os.getenv('file_path', 'Data_file_indecate.csv')
data_df = pd.read_csv(file_path)

# Map TRL text values to numerical values
TRL_mapping = {
    'Low: 3 - 4': 1,
    'Medium: 6 - 7': 2,
    'High: 8': 3,
    'High: 9': 4
}
data_df['TRL_num'] = data_df['TRL'].map(TRL_mapping)

# Mapping dictionary for technology values
technology_mapping = {
    1: "NG-fired",
    2: "NG-Oxyfuel",
    3: "Hybrid",
    4: "All-Electric",
    5: "H2-fired"
}

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
        # Header
        html.Header([
            html.H1("Decarbonisation Analysis of Flat Glass Production",
                    style={'font-size': '30px', 'font-weight': 'bold', 'font-family': 'Segoe UI', 'text-align': 'center', 'padding': '20px', 'backgroundColor': '#f2f2f2'}),
            html.Div([
                html.P([
                    html.B("List of Technologies: "),
                    dcc.Link("NG-fired Furnace", href='/ng-fired', style={'color': '#007bff'}),
                    ", ",
                    dcc.Link("NG-Oxyfuel Furnace", href='/ng-oxyfuel', style={'color': '#007bff'}),
                    ", ",
                    dcc.Link("Hybrid Furnace (Electric boosting)", href='/hybrid', style={'color': '#007bff'}),
                    ", ",
                    dcc.Link("All Electric Furnace", href='/all-electric', style={'color': '#007bff'}),
                    ", ",
                    dcc.Link(["H", html.Sub("2"), "-fired Furnace"], href='/h2-fired', style={'color': '#007bff'})
                ], style={'text-align': 'center'}),
                html.Br(),
                html.I("Carbon Capture and Heat Recovery is included in all technologies", style={'font-style': 'italic', 'color': '#6c757d'})
            ], style={'margin': '10px'})
        ], style={'backgroundColor': '#f8f9fa'}),

        # Content Section
        html.Div([
            # Parallel Coordinates Plot
            dcc.Graph(id='parallel-coordinates-plot',
                      style={'width': '100%', 'height': '525px', 'margin': '20px auto'}),

            # Technology Toggle Buttons (using dcc.Checklist)
            html.Div([
                dcc.Checklist(
                    id='Technology-toggle',
                    options=[{'label': technology_mapping[val], 'value': val} for val in data_df['Technology'].unique()],
                    value=data_df['Technology'].unique().tolist(),  # Set default value to show all technologies
                    inline=True,
                    style={'font-family': 'Segoe UI', 'margin': '20px', 'display': 'flex', 'justify-content': 'center'}
                )
            ], style={'text-align': 'center'}),

            # Input Blocks
            html.Div([
                html.Div([
                    html.Label('cEE Range'),
                    dcc.Input(
                        id='cEE-min-input',
                        type='number',
                        value=data_df['cEE'].min(),
                        style={'width': '70px', 'font-family': 'Segoe UI', 'margin': '0 5px'}
                    ),
                    dcc.Input(
                        id='cEE-max-input',
                        type='number',
                        value=data_df['cEE'].max(),
                        style={'width': '70px', 'font-family': 'Segoe UI', 'margin': '0 5px'}
                    )
                ], style={'display': 'inline-block', 'margin': '10px'}),

                html.Div([
                    html.Label('cH2 Range'),
                    dcc.Input(
                        id='cH2-min-input',
                        type='number',
                        value=data_df['cH2'].min(),
                        style={'width': '70px', 'font-family': 'Segoe UI', 'margin': '0 5px'}
                    ),
                    dcc.Input(
                        id='cH2-max-input',
                        type='number',
                        value=data_df['cH2'].max(),
                        style={'width': '70px', 'font-family': 'Segoe UI', 'margin': '0 5px'}
                    )
                ], style={'display': 'inline-block', 'margin': '10px'}),

                html.Div([
                    html.Label('cNG Range'),
                    dcc.Input(
                        id='cNG-min-input',
                        type='number',
                        value=data_df['cNG'].min(),
                        style={'width': '70px', 'font-family': 'Segoe UI', 'margin': '0 5px'}
                    ),
                    dcc.Input(
                        id='cNG-max-input',
                        type='number',
                        value=data_df['cNG'].max(),
                        style={'width': '70px', 'font-family': 'Segoe UI', 'margin': '0 5px'}
                    )
                ], style={'display': 'inline-block', 'margin': '10px'}),

                html.Div([
                    html.Label(['CO', html.Sub('2'), ' tax']),
                    dcc.Input(
                        id='cCO2-min-input',
                        type='number',
                        value=data_df['cCO2'].min(),
                        style={'width': '70px', 'font-family': 'Segoe UI', 'margin': '0 5px'}
                    ),
                    dcc.Input(
                        id='cCO2-max-input',
                        type='number',
                        value=data_df['cCO2'].max(),
                        style={'width': '70px', 'font-family': 'Segoe UI', 'margin': '0 5px'}
                    )
                ], style={'display': 'inline-block', 'margin': '10px'})
            ], style={'text-align': 'center'}),

            # Percentage Relative Occurrence
            html.Div(id='percentage-relative-occurrence', style={'margin': '20px', 'font-family': 'Segoe UI'})
        ], style={'padding': '20px', 'backgroundColor': '#ffffff'}),

        # Footer
        html.Footer([
            html.Div([
                html.P("©2024 Industrial Decarbonisation Analysis. All rights reserved.",
                       style={'font-size': '14px', 'color': '#6c757d', 'text-align': 'center', 'padding': '10px'}),
            ], style={'backgroundColor': '#f8f9fa'})
        ])
    ])

# Create a function to generate the description page layout
def description_layout(title, description):
    return html.Div([
        dcc.Link('Back to main page', href='/'),
        html.H2(title, style={'font-family': 'Segoe UI'}),
        html.P(description, style={'font-family': 'Segoe UI'})
    ], style={'padding': '20px'})

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

# Define the callback to update the plot and percentage occurrence
@app.callback(
    Output('parallel-coordinates-plot', 'figure'),
    Output('percentage-relative-occurrence', 'children'),
    [Input('Technology-toggle', 'value'),
     Input('cEE-min-input', 'value'),
     Input('cEE-max-input', 'value'),
     Input('cH2-min-input', 'value'),
     Input('cH2-max-input', 'value'),
     Input('cNG-min-input', 'value'),
     Input('cNG-max-input', 'value'),
     Input('cCO2-min-input', 'value'),
     Input('cCO2-max-input', 'value')]
)
def update_plots(selected_commodities, cEE_min, cEE_max, cH2_min, cH2_max, cNG_min, cNG_max, cCO2_min, cCO2_max):
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
    total_count = filtered_data.shape[0]
    if total_count > 0:
        Technology_counts = filtered_data['Technology'].value_counts()
        # Prepare the output
        occurrence_info = []
        for technology, count in Technology_counts.items():
            tech_name = technology_mapping[technology]
            tech_data = filtered_data[filtered_data['Technology'] == technology]
            # Find the set of costs for each technology
            cost_sets = {
                'cEE': sorted(tech_data['cEE'].unique()),
                'cH2': sorted(tech_data['cH2'].unique()),
                'cNG': sorted(tech_data['cNG'].unique()),
                'cCO2': sorted(tech_data['cCO2'].unique())
            }
            occurrence_info.append(
                html.Div([
                    html.Div([
                        html.H4(f"Technology: {tech_name}", style={'font-weight': 'bold', 'color': '#0056b3'}),
                        html.P(f"Number of occurrences: {count}", style={'font-size': '14px', 'color': '#333'}),
                        html.P(f"cEE: {cost_sets['cEE']}", style={'font-size': '12px', 'color': '#6c757d'}),
                        html.P(f"cH2: {cost_sets['cH2']}", style={'font-size': '12px', 'color': '#6c757d'}),
                        html.P(f"cNG: {cost_sets['cNG']}", style={'font-size': '12px', 'color': '#6c757d'}),
                        html.P(f"cCO2: {cost_sets['cCO2']}", style={'font-size': '12px', 'color': '#6c757d'})
                    ], style={'padding': '10px', 'backgroundColor': '#f8f9fa', 'border-radius': '5px', 'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)', 'width': '200px'})
                ], style={'margin-right': '15px', 'flex-shrink': '0'})
            )
        # Prepare the main output
        percentage_occurrence = html.Div([
            html.H3("Details", style={'font-family': 'Segoe UI', 'font-size': '22px', 'font-weight': 'bold', 'color': '#0056b3'}),
            html.P(f"Total number of solutions in the selected range: {total_count}", style={'font-size': '16px', 'color': '#495057'}),
            html.Br(),
            html.Div(occurrence_info, style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '15px', 'padding': '10px', 'justify-content': 'center'})
        ], style={'margin-bottom': '20px', 'font-family': 'Segoe UI'})
    else:
        percentage_occurrence = html.Div([
            html.H3("Details", style={'font-family': 'Segoe UI', 'font-size': '22px', 'font-weight': 'bold', 'color': '#0056b3'}),
            html.P("No data available for the selected range.", style={'font-size': '16px', 'color': '#6c757d'})
        ], style={'margin-bottom': '20px', 'font-family': 'Segoe UI'})

    # Create the parallel coordinates plot
    fig = go.Figure(data=
        go.Parcoords(
            line=dict(color=filtered_data['Technology'], colorscale='Blackbody'),
            dimensions=[
                dict(range=[data_df['EI'].min(), data_df['EI'].max()], tickvals=data_df['EI'].unique(), label='Emissions Impact: tCO2/tglass', values=filtered_data['EI']),
                dict(range=[1, 4], tickvals=[1, 2, 3, 4], ticktext=['Low: 3 - 4', 'Medium: 6 - 7', 'High: 8', 'High: 9'], label='TRL', values=filtered_data['TRL_num']),
                dict(range=[1, 5], tickvals=[1, 2, 3, 4, 5], ticktext=['NG-fired', 'NG-Oxyfuel', 'Hybrid', 'All-Electric', 'H2-fired'], label='<b>Technology</b>', values=filtered_data['Technology']),
                dict(range=[data_df['cCO2'].min(), data_df['cCO2'].max()], tickvals =[80, 150, 250, 350], label='Cost of Emissions (€/tCO2)', values=filtered_data['cCO2']),
                dict(range=[data_df['cEE'].min(), data_df['cEE'].max()], tickvals=[0.001, 0.01, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2], label='Cost of Electricity (€/kWh)', values=filtered_data['cEE']),
                dict(range=[data_df['cH2'].min(), data_df['cH2'].max()], tickvals=[0.001, 0.01, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2], label='Cost of Hydrogen (€/kWh)', values=filtered_data['cH2']),
                dict(range=[data_df['cNG'].min(), data_df['cNG'].max()], tickvals=[0.01, 0.035, 0.075, 0.1], label='Cost of Natural Gas (€/kWh)', values=filtered_data['cNG'])
            ],
            unselected = dict(line = dict(color = 'green', opacity = 0.0))
        )
    )

    return fig, percentage_occurrence

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)