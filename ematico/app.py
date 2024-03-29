import argparse
import dash_bootstrap_components as dbc
from dash import (
    Dash,
    html,
    dcc,
    page_container,
    Output,
    Input,
)
from layout import components
from data import load
import json


def create_app(file_path):
    app = Dash(
        external_stylesheets=[dbc.themes.DARKLY],
        external_scripts=[{"src": "https://cdn.tailwindcss.com"}],
        update_title=None,
        title="Ematico – Dashboard",
        use_pages=True,
    )

    df, df_rif, categories = load.load_data(file_path)
    sidebar = components.build_sidebar(categories)
    navbar = components.build_navbar(df)
    main = components.build_main(sidebar, page_container)

    # main = components.build_main_new(sidebar, page_container)

    app.layout = html.Div(
        [
            dcc.Store(id="df", data=df.to_json()),
            dcc.Store(id="df_rif", data=df_rif.to_json()),
            dcc.Store(id="categories", data=categories),
            navbar,
            main,
        ],
        className="font-sans",
        style={"font-family": "'Nunito'"},
    )
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ematico, interactive visualization of blood test results."
    )
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="Path to the Excel file"
    )
    parser.add_argument("-p", "--port", type=int, required=True, help="Port number")
    args = parser.parse_args()

    app = create_app(args.file)
    app.run(debug=False, host="0.0.0.0", port=args.port)
