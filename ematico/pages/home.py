import dash
from dash import html, Input, Output, callback
import pandas as pd
from layout import components

dash.register_page(__name__, order=1, path="/", title="Ematico Dashboard")


def layout():
    return html.Div(id="page-home", className="grid grid-cols-1 gap-3")


@callback(
    Output("page-home", "children"),
    Input("df", "data"),
    Input("df_rif", "data"),
    Input("categories", "data"),
)
def update_home(df, df_rif, categories):
    df = pd.read_json(df, convert_dates=["Data"])
    df_rif = pd.read_json(df_rif)

    return components.build_home_dashboard(df, df_rif, categories)
