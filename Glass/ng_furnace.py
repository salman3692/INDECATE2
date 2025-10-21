from dash import html

def description_layout():
    return html.Div([
        html.H2("NG-fired Furnace"),
        html.P("NG-fired furnaces use natural gas as the primary fuel source to heat the glass. They are commonly used in the industry due to the relatively low cost and availability of natural gas."),
        html.Img(src='/assets/float.jpg', style={'width': '600px'})  # Ensure you place the image in the assets folder
    ])
