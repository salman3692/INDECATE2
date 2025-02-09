import pandas as pd
import plotly.graph_objects as go
import dash
import os
from dash import dcc, html, Input, Output
import ng_furnace as ng_fired

# Enter your file path to read the data from the CSV file into a Pandas DataFrame
file_path = os.getenv('file_path', r'Data_file_indecate.csv')
data_df = pd.read_csv(file_path)

# Mapping dictionary for technology values
technology_mapping = {
    1: "NG-fired",
    2: "NG-Oxyfuel",
    3: "Hybrid",
    4: "All-Electric",
    5: "H2-fired"
}

external_stylesheets = [
"https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;600&display=swap"
]

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Create a function to generate the main page layout
def main_layout():
    return html.Div([

        # Technology Toggle Buttons (using dcc.Checklist)
        html.Div([
            # Add a label above the checklist
            html.H3("Select one or more technologies to compare", style={
                'font-family': 'Familjen Grotesk, sans-serif',
                'text-align': 'left',
                'margin-left': '42px',  # Adjust the left margin as needed
                'margin-bottom': '5px',  # Add some space between the label and checklist
                'color': '#003366'  # Optional: customize the color
            }),

        # The checklist itself
        dcc.Checklist(
            id='Technology-toggle',
            options=[{'label': technology_mapping[val], 'value': val} for val in data_df['Technology'].unique()],
            value=data_df['Technology'].unique().tolist(),  # Set default value to show all technologies
            inline=True,
            style={'font-family': 'Familjen Grotesk, sans-serif', 'margin-left': '38px','margin-top': '20px','margin-bottom': '20px', 'display': 'flex', 'justify-content': 'left'})
        ], style={'text-align': 'left'}),  # Set the parent div to left-align all child elements

        # Input Blocks
        html.Div([
            # Add a label above the checklist
            html.H3("Select Prices of Energy Sources and Emissions below to create custom Scenarios", style={
            'font-family': 'Familjen Grotesk, sans-serif',
            'text-align': 'left',
            'margin-left': '10px',  # Adjust the left margin as needed
            'margin-bottom': '5px',  # Add some space between the label and checklist
            'color': '#003366'  # Optional: customize the color
        }),

        html.Div([
            html.Label('Electricity Cost (€/MWh)',style={ 'font-family': 'Familjen Grotesk, sans-serif'}),
            dcc.Input(
                id='cEE-min-input',
                type='number',
                value=data_df['cEE'].min(),
                style={'width': '70px', 'font-family': 'Familjen Grotesk, sans-serif', 'margin': '0 5px'}
            ),
            dcc.Input(
                id='cEE-max-input',
                type='number',
                value=data_df['cEE'].max(),
                style={'width': '70px', 'font-family': 'Familjen Grotesk, sans-serif', 'margin': '0 5px'}
            )
        ], style={'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label(['H', html.Sub('2'), ' Cost (€/MWh)'],style={ 'font-family': 'Familjen Grotesk, sans-serif'}),
            dcc.Input(
                id='cH2-min-input',
                type='number',
                value=data_df['cH2'].min(),
                style={'width': '70px', 'font-family': 'Familjen Grotesk, sans-serif', 'margin': '0 5px'}
            ),
            dcc.Input(
                id='cH2-max-input',
                type='number',
                value=data_df['cH2'].max(),
                style={'width': '70px', 'font-family': 'Familjen Grotesk, sans-serif', 'margin': '0 5px'}
            )
        ], style={'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label('NG Cost (€/MWh)',style={ 'font-family': 'Familjen Grotesk, sans-serif'}),
            dcc.Input(
                id='cNG-min-input',
                type='number',
                value=data_df['cNG'].min(),
                style={'width': '70px', 'font-family': 'Familjen Grotesk, sans-serif', 'margin': '0 5px'}
            ),
            dcc.Input(
                id='cNG-max-input',
                type='number',
                value=data_df['cNG'].max(),
                style={'width': '70px', 'font-family': 'Familjen Grotesk, sans-serif', 'margin': '0 5px'}
            )
        ], style={'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label(['CO',html.Sub('2'),' Cost (€/tCO',html.Sub('2'),')'],style={ 'font-family': 'Familjen Grotesk, sans-serif'}),
            dcc.Input(
                id='cCO2-min-input',
                type='number',
                value=data_df['cCO2'].min(),
                style={'width': '70px', 'font-family': 'Familjen Grotesk, sans-serif', 'margin': '0 5px'}
            ),
            dcc.Input(
                id='cCO2-max-input',
                type='number',
                value=data_df['cCO2'].max(),
                style={'width': '70px', 'font-family': 'Familjen Grotesk, sans-serif', 'margin': '0 5px'}
            )
        ], style={'display': 'inline-block', 'margin': '10px'})
        ], style={'text-align': 'left','margin-left': '30px'}),

        # Parallel Coordinates Plot
        html.Div([
            dcc.Graph(id='parallel-coordinates-plot',
                    style={'width': '100%', 'height': '400px', 'margin': '0px'}), #originally 525px for website

            # Percentage Relative Occurrence
        html.Div(id='percentage-relative-occurrence', style={'margin': '20px', 'font-family': 'Familjen Grotesk, sans-serif'})
        ], style={'padding': '20px', 'backgroundColor': '#ffffff'}),

        # Footer
        html.Footer([
            html.Div([
                html.P("©2024 Industrial Decarbonisation Analysis. All rights reserved.",
                    style={'font-size': '14px', 'color': '#6c757d', 'text-align': 'center', 'padding': '10px'}),
            ], style={'backgroundColor': '#003366'})
        ])
    ])

# Create a function to generate the description page layout
def description_layout(title, description):
    return html.Div([
        dcc.Link('Back to main page', href='/'),
        html.H2(title, style={'font-family': 'Familjen Grotesk, sans-serif'}),
        html.P(description, style={'font-family': 'Familjen Grotesk, sans-serif'})
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

@app.callback(
    [Output('line-1', 'style')],
    [Input('line-1-length-slider', 'value')]
)
def update_lines(length_1, length_2, length_3):
    # Update the width of each line based on the slider value
    line_1_style = {'height': '10px', 'background-color': 'blue', 'width': f'{length_1}px', 'margin-top': '10px'}
    return line_1_style

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
        # Prepare the occurrence info for details section
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
                        html.H4(f"Technology: {tech_name}", style={'font-weight': 'bold', 'color': '#003366'}),
                        html.P(f"Number of occurrences: {count}", style={'font-size': '14px', 'color': '#333'}),
                        html.P(f"cEE: {cost_sets['cEE']}", style={'font-size': '12px', 'color': '#6c757d'}),
                        html.P(f"cH2: {cost_sets['cH2']}", style={'font-size': '12px', 'color': '#6c757d'}),
                        html.P(f"cNG: {cost_sets['cNG']}", style={'font-size': '12px', 'color': '#6c757d'}),
                        html.P(f"cCO2: {cost_sets['cCO2']}", style={'font-size': '12px', 'color': '#6c757d'})
                    ], style={'padding': '10px', 'backgroundColor': '#f8f9fa', 'border-radius': '5px', 'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)', 'width': '200px'})
                ], style={'margin-right': '15px', 'flex-shrink': '0'})
            )

        # Prepare the line scatter plot
        scatter_data = [go.Scatter(
            x=[technology_mapping[val] for val in Technology_counts.index],
            y=Technology_counts.values,
            mode='lines+markers',
            marker=dict(size=10, color='blue', line=dict(width=2, color='darkblue')),
            line=dict(color='blue', width=2),
            name='Occurrences'
        )]
        scatter_layout = go.Layout(
            title='Number of Occurrences of Each Technology',
            xaxis=dict(
                title='Technology',
                tickvals=list(range(len(Technology_counts.index))),
                ticktext=[technology_mapping[val] for val in Technology_counts.index],
                showline=True,
                linecolor='black',
                linewidth=2,
                mirror=True  # Show the line on both sides of the plot
            ),
            yaxis=dict(
                title='Number of Occurrences',
                range=[0, max(Technology_counts.values) * 1.1],  # Add some padding above the highest value
                showline=True,
                linecolor='black',
                linewidth=2,
                mirror=True,  # Show the line on both sides of the plot
            ),
            font=dict(family='Familjen Grotesk, sans-serif'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=50, r=20, t=50, b=50),
            xaxis_title_font=dict(size=14, color='#003366'),
            yaxis_title_font=dict(size=14, color='#003366'),
            xaxis_tickfont=dict(size=12),
            yaxis_tickfont=dict(size=12)
        )
        scatter_fig = go.Figure(data=scatter_data, layout=scatter_layout)

        # Prepare the main output
        percentage_occurrence = html.Div([
            html.H3("Details", style={'font-family': 'Familjen Grotesk, sans-serif', 'font-size': '22px', 'font-weight': 'bold', 'color': '#003366'}),
            html.P(f"Total number of solutions in the selected range: {total_count}", style={'font-size': '16px', 'color': '#495057'}),
            html.Br(),
            dcc.Graph(id='technology-occurrence-plot', figure=scatter_fig, style={'width': '100%', 'height': '400px'}),
            html.Br(),
            html.Div(occurrence_info, style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '15px', 'padding': '10px', 'justify-content': 'center'}),
        ], style={'margin-bottom': '20px', 'font-family': 'Familjen Grotesk, sans-serif'})
    else:
        percentage_occurrence = html.Div([
            html.H3("Details", style={'font-family': 'Familjen Grotesk, sans-serif', 'font-size': '22px', 'font-weight': 'bold', 'color': '#003366'}),
            html.P("No data available for the selected range.", style={'font-size': '16px', 'color': '#6c757d'})
        ], style={'margin-bottom': '20px', 'font-family': 'Familjen Grotesk, sans-serif'})

    # Create the parallel coordinates plot
    fig = go.Figure(data=
    go.Parcoords(
        line=dict(
            color=filtered_data['Technology'], colorscale='blackbody'),
        dimensions=[
            dict(range=[data_df['cEE'].min(), data_df['cEE'].max()], tickvals=[10, 25, 50, 75, 100, 125, 150, 175, 200], label='Electricity<br>(€/MWh)', values=filtered_data['cEE']),
            dict(range=[data_df['cH2'].min(), data_df['cH2'].max()], tickvals=[10, 25, 50, 75, 100, 150, 200], label='Hydrogen<br>(€/MWh)', values=filtered_data['cH2']),
            dict(range=[data_df['cNG'].min(), data_df['cNG'].max()], tickvals=[10, 35, 55, 75, 100], label='NG<br>(€/MWh)', values=filtered_data['cNG']),
            dict(range=[75,250], tickvals =[75, 100, 150, 200, 250], label='Emissions<br>(€/tCO₂)', values=filtered_data['cCO2']),
            dict(range=[1, 5], tickvals=[1, 2, 3, 4, 5], ticktext=['NG-fired','NG-Oxyfuel','Hybrid','All-Electric','H2-fired'], label='<b>Technology</b>', values=filtered_data['Technology']),
            # dict(range=[data_df['fuel_demand'].min(), data_df['fuel_demand'].max()], tickvals=[round(val, 2) for val in data_df['fuel_demand'].unique()], label='Fuel Demand<br>(GJ/t<sub>glass</sub>)', values=filtered_data['fuel_demand']),
            # dict(range=[data_df['elec_demand'].min(), data_df['elec_demand'].max()], tickvals=[round(val, 2) for val in data_df['elec_demand'].unique()], label='Electricity Demand<br>(GJ/t<sub>glass</sub>)', values=filtered_data['elec_demand']),
            dict(range=[1,7], tickvals=[1, 2, 3, 4, 5, 6, 7], label='Fuel Demand<br>(GJ/t<sub>glass</sub>)', values=filtered_data['fuel_demand']),
            dict(range=[0,5], tickvals=[0, 1, 2, 3, 4, 5], label='Electricity Demand<br>(GJ/t<sub>glass</sub>)', values=filtered_data['elec_demand']),
            dict(range=[1, 4], tickvals=[1, 2, 3, 4], ticktext=[' ','Yes','No',' '], label='Carbon<br>Capture', values=filtered_data['co2_capt']),
            # dict(range=[data_df['EI'].min(), data_df['EI'].max()], tickvals=[round(val, 2) for val in data_df['EI'].unique()], label='Emissions<br>(t<sub>CO2</sub>/t<sub>glass</sub>)', values=filtered_data['EI'].round(2))
            dict(range=[0.1,0.7], tickvals=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], label='Emissions<br>(t<sub>CO2</sub>/t<sub>glass</sub>)', values=filtered_data['EI'].round(2))
        ],
        unselected=dict(line=dict(color='green', opacity=0.0))
    )
    )

    fig.update_layout(
        title_font=dict(size=20, color='#003366'),
        font=dict(family='Familjen Grotesk, sans-serif', size=15),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickangle=-45),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=50, r=40, t=50, b=50)
    )
    return fig, percentage_occurrence

# for deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=True, host='0.0.0.0', port=port)

# # Run the app locally
# if __name__ == '__main__':
#     app.run_server(debug=True)


##################################################################
# extras below:
# Div for both lines
# html.Div([
#     # First line (left side with arrows and centered text)
#     html.Div([html.Label("Inputs", className="centered-text"),  # Apply 'centered-text' class to move the label above the line
#               html.Div(style={'position': 'relative','height': '2px','background-color': 'lightgrey',
#               'width': '750px','margin-left': '35px','margin-top': '50px',}, className="arrow-line")],
#               style={'position': 'relative', 'width': '750px'}  # Wrap div to control width and relative position),

#         # Second line (right side with arrows and centered text)
#         html.Div(
#             [
#                 html.Label("Outputs", className="centered-text"),  # Apply 'centered-text' class to move the label above the line
#                 html.Div(style={
#                     'position': 'relative',
#                     'height': '2px',
#                     'background-color': 'lightgrey',
#                     'width': '750px',  # Adjust the width if necessary
#                     'margin-right': '65px',
#                     'margin-top': '50px',
#                 }, className="arrow-line")
#             ],
#             style={'position': 'relative', 'width': '750px','margin-right': '50px' }  # Wrap div to control width and relative position
#         )
# ], 
# style={
#     'display': 'flex',
#     'flex-direction': 'row',  # Make them appear next to each other
#     'justify-content': 'space-between',  # Space them out evenly
#     'margin-bottom': '0px'
# }),
