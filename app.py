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

    app.layout = html.Div(
        [
            dcc.Store(id="df", data=df.to_json()),
            dcc.Store(id="df_rif", data=df_rif.to_json()),
            dcc.Store(id="categories", data=categories),
            navbar,
            main,
        ],
        className="font-sans",
    )
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Your script description.")
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="Path to the Excel file"
    )
    args = parser.parse_args()

    app = create_app(args.file)
    app.run(debug=True)
