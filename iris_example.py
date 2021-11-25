# required imports
import dash # 2.0.0 <- will not work with earier versions
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly # 5.3.1
import plotly.express as px
import plotly.graph_objects as go

# read in iris dataset and plot the initial graph, colored by species
df = px.data.iris()
fig = px.scatter(df, x='sepal_length', y='sepal_width', color='species')

# define the app layout
app = dash.Dash(__name__)
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Update Selected Points"),
            html.H4("Minimal working example--Iris"),
            html.H6("""Fixed! Selecting point from the dropdown now selected only that point
rather than that point for each species :)"""),
            html.Hr()
            ])
        ]),
    dbc.Row([
        dbc.Col([
            # similified dropdown to select df indices
            dcc.Dropdown(
                id='iris-dropdown',
                options = [{'label': x, 'value': x} for x in range(len(df))],
                multi=True,
                placeholder="Select point indices"                
                ),
            # the graph to be updated
            dcc.Graph(
                id='iris-scatter',
                figure=fig
                )
            ])
        ])
    ])

# simplified callback
@app.callback(
    Output('iris-scatter', 'figure'),
    Input('iris-scatter', 'figure'),
    Input('iris-dropdown', 'value')
    )
def update_plot(fig_old, selection):
    """
    Take in the point(s) to be selected from the dropdown and highlight them on the graph
    If no points are selected, then highlight all points
      ARGS:
            fig_old -- the current figure to be updated
            selection -- the points to be highlighted

    RETURN:
            the plot with updated selection
    
    """

    # select all points were selection is empty/unspecified
    if (selection is None) or (len(selection) == 0):
        points = [i for i in range(len(df))]
        fig = go.Figure(fig_old)
        fig.update_traces(selectedpoints=points)

    # select only the intended points
    else:

        # extract esch groups dict from the figure dict
        groups = [i for i in fig_old['data']]
        k = None

        # iterate over groups (species)
        for gi, group in enumerate(groups):
            xi = [i for i in range(len(group['x']))]             # point indices for the group (using x-coords)
            k = xi if k is None else [i + k[-1] + 1 for i in xi] # absolute point indices

            # select group indices where corresponding absolute indices are selected
            group_points = [xi[i] for i, p in enumerate(k) if p in selection]  
            fig_old['data'][gi]['selectedpoints'] = group_points # update the group dict

        # read the dict as plotly figure for futher use
        fig = go.Figure(fig_old)

    fig.update_layout(uirevision="Don't Change")

    return fig
    

if __name__ == "__main__":
    print(dash.__version__)
    print(plotly.__version__)
    app.run_server(debug=True)
