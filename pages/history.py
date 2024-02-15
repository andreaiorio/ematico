import dash
from dash import html, Input, Output, callback
import pandas as pd
from layout import components

dash.register_page(__name__, order=2)


def layout():
    return html.Div(id="page-history", className="grid grid-cols-1 gap-3")


@callback(
    Output("page-history", "children"),
    Input("df", "data"),
    Input("df_rif", "data"),
    Input("categories", "data"),
)
def update_time(df, df_rif, categories):
    df = pd.read_json(df, convert_dates=["Data"])
    df_rif = pd.read_json(df_rif)

    return components.build_time_plots(df, df_rif, categories)
