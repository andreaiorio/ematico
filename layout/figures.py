from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

from layout.utils import (
    get_min_max_threshold,
    get_label,
    make_slug,
    get_percentage,
    get_last_date_test,
)


def draw_plot(test, color, df, df_rif):
    min_y, max_y = get_min_max_threshold(test, df, df_rif)
    return html.Div(
        [
            html.H4(test, className="font-bold uppercase text-xs tracking-widest"),
            html.Div(
                [
                    dcc.Graph(
                        figure=px.line(
                            df,
                            x="Data",
                            y=test,
                            height=150,
                            markers=True,
                            line_shape="spline",
                            range_y=[min_y, max_y],
                        )
                        .update_layout(
                            yaxis_title=None,
                            template="plotly_dark",
                            margin={"t": 0, "l": 0, "b": 0, "r": 0},
                            plot_bgcolor="rgba(0, 0, 0, 0)",
                            paper_bgcolor="rgba(0, 0, 0, 0)",
                            # yaxis_range=[float(df_rif[test][0]), float(df_rif[test][1])],
                            # Set the desired height in pixels
                        )
                        .update_yaxes(
                            ticksuffix=" " + get_label(test, df_rif), showgrid=False
                        )
                        .update_xaxes(showgrid=False)
                        .update_traces(
                            connectgaps=True,
                            # Set the line color for this plot
                            line=dict(color=color),
                        )
                        .add_hline(
                            y=df_rif[test][0],
                            line_width=1,
                            line_dash="dash",
                            line_color="green",
                        )
                        .add_hline(
                            y=df_rif[test][1],
                            line_width=1,
                            line_dash="dash",
                            line_color="green",
                        ),
                        config={"displayModeBar": False},
                    )
                ],
                className="mt-2",
            ),
        ],
        className="rounded-xl bg-neutral-800 p-4",
    )


def draw_card(test, category, df, df_rif):
    last_value = df[test].dropna().tail(1).values[0]
    vmin, vmax = get_min_max_threshold(test, df, df_rif)
    percentage = get_percentage(last_value, test, df, df_rif)

    if 25 <= percentage <= 75:
        circle_color = "green"

    elif 10 <= percentage < 25 or 75 < percentage <= 90:
        circle_color = "orange"

    else:
        circle_color = "red"

    card = html.Div(
        [
            html.Div(
                html.Div(
                    [
                        html.H3(test, className=""),
                        html.P(
                            f"{get_last_date_test(test, df)}",
                            className="text-xs text-slate-500 mt-1",
                        ),
                    ]
                ),
                className="col-span-1",
            ),
            html.Div(
                html.Div(
                    [
                        html.Big(
                            f"{last_value}",
                            className=f"text-{circle_color}-300",
                        ),
                        html.Br(),
                        html.Small(
                            f"{df_rif[test][2]}",
                            className=f"text-{circle_color}-200",
                        ),
                    ]
                ),
                className="col-span-1 text-center",
            ),
            html.Div(
                html.Div(
                    className="rounded-xl shadow-sm overflow-hidden p-3 h-[100%] bg-neutral-800 mr-3",
                    children=[
                        html.Div(
                            className="flex items-center justify-left",
                            children=[
                                html.Div(
                                    children="Low",
                                    className="inline-block w-[15%] opacity-100 inline-block w-[10%] text-xs text-center uppercase font-bold",
                                ),
                                html.Div(
                                    children="Below average",
                                    className="inline-block w-[15%] opacity-100 inline-block w-[15%] text-xs text-center uppercase font-bold",
                                ),
                                html.Div(
                                    children="Optimal",
                                    className="inline-block w-[15%] opacity-100 inline-block w-[50%] text-xs text-center uppercase font-bold",
                                ),
                                html.Div(
                                    children="Above average",
                                    className="inline-block w-[15%] opacity-100  inline-block w-[15%] text-xs text-center uppercase font-bold",
                                ),
                                html.Div(
                                    children="High",
                                    className="inline-block w-[15%] opacity-100 inline-block w-[10%] text-xs text-center uppercase font-bold",
                                ),
                            ],
                        ),
                        html.Div(
                            className="flex items-center justify-left gap-1 h-2 mt-1 relative",
                            children=[
                                html.Div(
                                    className=f"h-7 w-7 rounded-full absolute left-[{percentage}%] border-4 border-neutral-800 shadow-black bg-{circle_color}-400"
                                ),
                                html.Div(
                                    className="inline-block h-[100%] opacity-100 rounded-lg w-[10%] bg-red-200"
                                ),
                                html.Div(
                                    className="inline-block h-[100%] opacity-100 rounded-lg w-[15%] bg-orange-200"
                                ),
                                html.Div(
                                    className="inline-block h-[100%] opacity-100 rounded-lg w-[50%] bg-green-200"
                                ),
                                html.Div(
                                    className="inline-block h-[100%] opacity-100 rounded-lg w-[15%] bg-orange-200"
                                ),
                                html.Div(
                                    className="inline-block h-[100%] opacity-100 rounded-lg w-[10%] bg-red-200"
                                ),
                            ],
                        ),
                    ],
                ),
                className="col-span-4",
            ),
        ],
        className="mb-3 items-center grid grid-cols-6",
    )
    return card
