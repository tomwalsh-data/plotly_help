# plotly_help
Minimal working example of dash app using the iris dataset.

The goal: by selecting indices from the dropdown highlight the point(s) with those indices in the underlying dataframe
The problem: plotly currently highlights the points with those indices *for each species*

Example: Select index 0 from the dropdown
Current behaviour: plotly highlights three points on the graph--one of each colour/species
Desired behaviour: plotly highlights one point on the graph--whichever happens to be first in the dataframe--without considering colour/species

The solution: update the figure dict directly and pass the result to `go.Figure(fig_dict)`
Under the hood, a plotly figure is sotred as a dictionary with the form
    fig_dict = {
        'data': [group_0, group_1, group_3],
        etc...
    }
    
where `group_k` is a dictionary for that legend group
    
To get intended behaviour
    1. extract the group dictionaries
    2. get the indices of the points within the group (idices reset across groups)
    3. calculate the absolute indices of theose points within the full dataframe
    4. use this mapping to get only the group indices which correspond to the absolute indices
    5. update the group dictionary with the new values
    
pass to go.Figure()/return
