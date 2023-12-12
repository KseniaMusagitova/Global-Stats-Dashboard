from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1(children='Global Stats Dashboard', style={'textAlign': 'center'}),
    
    # Dropdown for selecting a country
    dcc.Dropdown(options=[{'label': country, 'value': country} for country in df['country'].unique()], 
                 value='Canada', id='dropdown-selection'),
    
    # Graph for displaying data
    dcc.Graph(id='graph-content'),
    
    # Div for displaying information about the selected point
    html.Div(id='selected-point-info'),
    
    # DataTable for displaying tabular data
    dash_table.DataTable(id='table-content')
])

# Define the callback function for updating the graph, info, and table
@app.callback(
    [Output('graph-content', 'figure'),
     Output('selected-point-info', 'children'),
     Output('table-content', 'data'),
     Output('table-content', 'columns')],
    [Input('dropdown-selection', 'value'),
     Input('graph-content', 'clickData')]
)
def update_graph_and_display_info(selected_country, click_data):

    global df
    
    # Filter the dataset based on the selected country
    dff = df[df['country'] == selected_country]
    
    # Create a line plot using Plotly Express
    fig = px.line(dff, x='year', y='pop', title=f'Population Over Time - {selected_country}')

    # Default information text
    info_text = "Click on a point to see information."

    # If there's click data and points in the click data, update the information text
    if click_data and 'points' in click_data and click_data['points']:
        selected_point = click_data['points'][0]
        year = selected_point['x']
        population = selected_point['y']
        info_text = f"In {year}, the population was {population} in {selected_country}."

    # Create data for the DataTable
    table_data = dff.to_dict('records')

    # Create columns for the DataTable
    table_columns = [{'name': col, 'id': col} for col in dff.columns]

    return fig, info_text, table_data, table_columns

# Run the app if this script is executed
if __name__ == '__main__':
    app.run_server(debug=True)
