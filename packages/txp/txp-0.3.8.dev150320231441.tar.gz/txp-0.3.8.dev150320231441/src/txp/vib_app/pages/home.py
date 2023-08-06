import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
import dash
from txp.vib_app.pages.styles import *

dash.register_page(__name__)

#####################################################
# Dash Components Declaration
# From here on, you'll see the declaration of components
# that are in the Vibration Analysis View.
# Components that requires input values to render, will be setup
# with the helper function "init_view_components"
#####################################################

dash.register_page(__name__, path='/')

layout=html.Div(
    "Hello World",
    id="vibration",
    style=CONTENT_STYLE
)
