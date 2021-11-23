# plotly_help
Minimal working example of dash app using the iris dataset.

The goal: by selecting indices from the dropdown highlight the point(s) with those indices in the underlying dataframe
The problem: plotly currently highlights the points with those indices *for each species*

Example: Select index 0 from the dropdown
Current behaviour: plotly highlights three points on the graph--one of each colour/species
Desired behaviour: plotly highlights one point on the graph--whichever happens to be first in the dataframe--without considering colour/species
