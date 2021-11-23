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
            html.H6("""Choosing points from the dropdown selects those points
for each species.\n Intended behaviour is to select only those points irrespective of species. \n 
e.g. point 0 should select only the first flower, but currently selects the first of each species"""),
            html.Hr()
            ])
        ]),
    dbc.Row([
        dbc.Col([
            # similified dropdown to select df indices
            dcc.Dropdown(
                id='iris-dropdown',
                options = [{'label': x, 'value': x} for x in range(10)],
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

    # read in the old figure for modification--"Don't Change" the zoom/pan on update
    fig = go.Figure(fig_old)
    fig.update_layout(uirevision="Don't Change")

    if (selection is None) or (len(selection) == 0):
        # no points are selected: highlight all
        points = [i for i in range(len(df))]

    else:
        # choose the selected points--more complicated in real app
        points = selection

    # update `selectedpoints`
    fig.update_traces(selectedpoints=points)

    """
    current result: selects the passed indices for each species
                    e.g. pass [0,1,2] currently selects the first three points for each species
                    -> 9 points highlighted (first 3 points for each of 3 species)

    desired result: select the passed indices from the dataframe only:
                    e.g. pass [0,1,2] to select the first three flowers, regardless of species
                    -> 3 points highlighted, color irrelevent.
    """

    return fig
    

if __name__ == "__main__":
    print(dash.__version__)
    print(plotly.__version__)
    app.run_server(debug=True)
