from dash import html, get_asset_url
import dash_bootstrap_components as dbc
import plotly.express as px

from layout.figures import draw_card, draw_plot
from layout.utils import get_min_max_threshold, get_label, make_slug, get_last_date


def build_sidebar(categories):
    sidebar = html.Aside(
        [
            html.H4(
                "Body systems",
                className="uppercase text-sm font-bold tracking-widest mb-3",
            ),
            dbc.Nav(
                [
                    dbc.NavLink(
                        category,
                        href=f"#{make_slug(category)}",
                        external_link=True,
                        className="p-2",
                    )
                    for category in categories
                ],
                vertical=True,
                pills=True,
                className="",
            ),
        ],
        className="self-start sticky top-10 col-span-1",
    )
    return sidebar


def build_header(df):
    return html.Header(
        [
            html.Img(src=get_asset_url("logo.svg"), className="h-12 cursor-pointer"),
            html.P(
                f"Last update: {get_last_date(df)}",
                className="text-sm text-gray-400",
            ),
        ],
        className="mb-8",
    )


def build_layout(df, df_rif, categories):
    header = build_header(df)
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

        dash_cards += [
            html.Div(
                [html.H3(category, className="text-2xl mb-3")] + [dash_group],
                className="bg-neutral-900 p-5 rounded-xl",
                id=f"{make_slug(category)}",
            )
        ]

    dash_cards = html.Div(dash_cards, className="grid grid-cols-1 gap-3")

    return [
        header,
        html.Main(
            [sidebar] + [html.Div([dash_cards] + [dash_list], className="col-span-6")],
            className="grid grid-cols-7",
        ),
    ]
