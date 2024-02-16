from dash import html, get_asset_url, page_registry, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from layout.figures import draw_card, draw_plot
from layout.utils import get_min_max_threshold, get_label, make_slug, get_last_date


def build_main(sidebar, page):
    return html.Main(
        [sidebar, html.Div(page, className="col-span-1 lg:col-span-5")],
        className="grid grid-cols-1 lg:grid-cols-6 px-6 gap-x-5 mt-4",
    )


def build_navbar(df):
    return html.Nav(
        [
            html.Div(
                [
                    html.Img(
                        src=get_asset_url("logo.svg"), className="h-7 cursor-pointer"
                    ),
                ],
                className="flex items-center flex-shrink-0 mr-6",
            ),
            html.Div(
                [
                    html.Ul(
                        [
                            html.Li(
                                [
                                    dcc.Link(
                                        f"{page['name']}",
                                        href=f'{page["relative_path"]}',
                                    )
                                ],
                                className="sm:inline-block sm:mt-0 text-gray-400 hover:text-white mr-4 rounded px-3 py-2",
                            )
                            for page in page_registry.values()
                        ],
                        className="text-sm lg:flex-grow",
                    ),
                ],
                className="w-full block flex-grow sm:flex sm:items-center sm:w-auto",
            ),
            html.Div(
                f"Last update: {get_last_date(df)}",
                className="inline-block text-xs text-right rounded text-gray-400 sm:mt-0",
            ),
        ],
        className="flex items-center justify-between flex-wrap lg:mb-5 bg-neutral-900 p-10",
    )


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
                        className="lg:px-2 lg:py-2 px-2 text-xs my-1 lg:text-sm  rounded inline-block !text-gray-400 hover:bg-neutral-900 hover:!text-white",
                    )
                    for category in categories
                ],
                vertical=True,
                pills=True,
                className="inline-block ml-2 mr-4",
            ),
        ],
        className="lg:self-start lg:sticky lg:top-10 mb-3 col-span-1",
    )
    return sidebar


def build_time_plots(df, df_rif, categories):
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
        dash_group = html.Div(
            dash_group,
            className=f"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-{cols} gap-3",
        )

        dash_list += [
            html.Div(
                [html.H3(category, className="text-2xl mb-3")] + [dash_group],
                className="bg-neutral-900 p-4 rounded-xl",
                id=f"{make_slug(category)}",
            )
        ]

    return dash_list


def build_home_dashboard(df, df_rif, categories):
    dash_cards = []
    for category in categories:
        dash_group = []
        for esame in categories[category]:
            vmin, vmax = get_min_max_threshold(esame, df, df_rif)
            dash_group += [draw_card(esame, category, df, df_rif)]
        dash_group = html.Div(
            dash_group, className="grid grid-cols-1 gap-3 xl:grid-cols-2"
        )

        dash_cards += [
            html.Div(
                [html.H3(category, className="text-2xl mb-3")] + [dash_group],
                className="bg-neutral-900 p-4 rounded-xl",
                id=f"{make_slug(category)}",
            )
        ]

    return dash_cards
