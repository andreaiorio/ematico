import argparse
import dash_bootstrap_components as dbc
from dash import Dash, html
from layout import components
from data import load


def create_app(file_path):
    app = Dash(
        external_stylesheets=[dbc.themes.DARKLY],
        external_scripts=[{"src": "https://cdn.tailwindcss.com"}],
    )
    df, df_rif, categories = load.load_data(file_path)
    layout = components.build_layout(df, df_rif, categories)
    app.layout = html.Div(layout)
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Your script description.")
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="Path to the Excel file"
    )
    args = parser.parse_args()

    app = create_app(args.file)
    app.run()
