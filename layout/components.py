from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px

from layout.figures import draw_card, draw_plot
from layout.utils import get_min_max_threshold, get_label, make_slug


def build_sidebar(categories):
    sidebar = html.Div(
        [
            html.H4(
                "Category",
                className="uppercase text-sm font-bold tracking-widest ml-5 mb-3",
            ),
            dbc.Nav(
                [
                    dbc.NavLink(
                        category, href=f"#{make_slug(category)}", active="exact"
                    )
                    for category in categories
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="fixed inset-0 w-64 py-2 px-1",
    )
    return sidebar


def build_header():
    return html.H1("Ematico dashboard", className="text-5xl font-sans mb-4 font-bold")


def build_layout(df, df_rif, categories):
    header = build_header()
    sidebar = build_sidebar(categories)

    color_scale = px.colors.qualitative.Set1
    colors = color_scale[: len(categories)]

    dash_list = []
    for color, category in zip(colors, categories):
        dash_group = []
        n_plots = len(categories[category])
        if n_plots <= 6:
            cols = n_plots
        else:
            cols = 5

        for esame in categories[category]:
            vmin, vmax = get_min_max_threshold(esame, df, df_rif)
            dash_group += [draw_plot(esame, color, df, df_rif)]
        dash_group = html.Div(dash_group, className=f"grid grid-cols-{cols} gap-3")

        dash_list += [html.H3(category, className="text-2xl mb-3 mt-5")] + [dash_group]

    dash_list = html.Div(dash_list)

    dash_cards = []
    for category in categories:
        dash_group = []
        for esame in categories[category]:
            vmin, vmax = get_min_max_threshold(esame, df, df_rif)
            dash_group += [draw_card(esame, category, df, df_rif)]
        dash_group = html.Div(dash_group, className="grid grid-cols-2 gap-3")

        dash_cards += [html.H3(category, className="text-2xl mb-3 mt-5")] + [dash_group]

    dash_cards = html.Div(dash_cards)

    return [
        dbc.Container(
            [sidebar] + [header] + [dash_cards] + [dash_list],
            fluid=True,
            className="ml-64 mt-4 py-2 px-2 w-auto",
        )
    ]
