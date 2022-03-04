import dash
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from plotly.graph_objects import Figure

import pandas as pd
from itertools import product

from figures import create_lineplot, create_barchart, create_feature_chart, create_scatter_plot, create_index_chart
from useful_func import get_lineplot_title, get_barchart_title, combi_breakdown

# Instantiate Dash app and server
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Residential Real Estate in Poland"

# Global variables
MARKETS = ["Primary market", "Secondary market"]
PRICES = ["Offer prices", "Transaction prices"]
CITIES = ['Białystok', 'Bydgoszcz', 'Gdańsk', 'Gdynia', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Łódź', 'Olsztyn',
          'Poznań', 'Rzeszów', 'Szczecin', 'Warszawa', 'Wrocław']
COMBINED = [" ".join(x) for x in list(product(*[MARKETS, PRICES, CITIES]))]
SLIDER_DATE_RANGE = pd.date_range(start='2006-09-30', end='2021-12-31', freq='3M')
CATEGORY = [dict(label="Return series", value="ret"),
            dict(label="Sentiment", value="sentiment"),
            dict(label="Risk measures", value="risk")]
INDICES = [dict(label="All cities", value="all")]
INDEX_TYPES = [dict(label="Equal weighted", value="equal_weighted"),
               dict(label="Price weighted", value="price_weighted")]
FIG_INIT = Figure(layout=dict(
    paper_bgcolor='#001540',
    plot_bgcolor='#001540',
    yaxis=dict(showgrid=False, fixedrange=True),
    xaxis=dict(showgrid=False, nticks=10, fixedrange=True),
    showlegend=False
), data=[])


# Layout
app.layout = dbc.Container(children=[
    html.H1("Residential real estate market in Poland"),
    html.Hr(),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardHeader("Controls"),
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        dbc.Col(children=[
                            html.Label('Price type selection: offer and/or transaction', id='label_price_drdwn_a'),
                            dcc.Checklist(
                                id="checklist_price_a",
                                options=[
                                    {'label': 'Transaction prices', 'value': 'tp'},
                                    {'label': 'Offer prices', 'value': 'op'}
                                ],
                                labelStyle={"margin-right": "1rem"},
                                inputStyle={"margin-right": "0.5rem"}
                            )], sm=4
                        ),
                        dbc.Col(children=[
                            html.Label('Price type selection: nominal or real', id='label_price_drdwn_b'),
                            dcc.RadioItems(
                                id="radio_price_b",
                                options=[
                                    {'label': 'Nominal', 'value': 'nom'},
                                    {'label': 'Real', 'value': 'real'}
                                ],
                                labelStyle={"margin-right": "1rem"},
                                inputStyle={"margin-right": "0.5rem"}
                            )], sm=4
                        ),
                        dbc.Col(children=[
                            html.Label('Plot type selection: actual or indexed', id='label_chart_drdwn'),
                            dcc.RadioItems(
                                id="radio_plot",
                                options=[
                                    {'label': 'Actual values', 'value': 'act'},
                                    {'label': 'Indexed values', 'value': 'ind'}
                                ],
                                labelStyle={"margin-right": "1rem"},
                                inputStyle={"margin-right": "0.5rem"}
                            )], sm=4
                        )], className="gy-3"
                    ),
                    dbc.Row(children=[
                        dbc.Col(children=[
                            html.Label('Local market selection', id='label_city_drdwn'),
                            dcc.RadioItems(
                                id="radio_cities",
                                options=[
                                    {"label": "Select all", "value": "all"},
                                    {"label": "Custom", "value": "custom"}
                                ],
                                labelStyle={"margin-right": "1rem"},
                                inputStyle={"margin-right": "0.5rem"}
                            )], md=12
                        ),
                        dbc.Col(children=[
                            dcc.Dropdown(
                                id='dropdown_multi_city',
                                options=[{'label': c, 'value': c} for c in CITIES],
                                multi=True,
                                searchable=False,
                                placeholder='Select town/city...'
                            )], md=12
                        ),
                        dbc.Col(children=[
                            html.Label('Select time range by dragging handles', id='label_slider'),
                            dcc.RangeSlider(
                                id='slider',
                                marks={
                                    i: {"label": f"Q{SLIDER_DATE_RANGE[i].quarter}-{SLIDER_DATE_RANGE[i].year}",
                                        "style": {"font-size": "14px", "margin-top": "5px"}} for i in
                                    range(len(SLIDER_DATE_RANGE))
                                    if i % 4 == 1
                                },
                                step=1,
                                min=0,
                                max=len(SLIDER_DATE_RANGE) - 1,
                                value=[0, len(SLIDER_DATE_RANGE) - 1]
                            )], md=12
                        )], className="gy-3"
                    )]
                )]
            )], md=12
        )]
    ),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardHeader("Primary market"),
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        html.Label(id="lineplot_pm_label",
                                   children="Primary market prices plot",
                                   className="text-center"),
                        dcc.Graph(id="lineplot_pm", figure=FIG_INIT)
                    ]),
                    dbc.Row(children=[
                        html.Label(id="barchart_pm_label",
                                   children="Primary market mean quarterly geometric return chart",
                                   className="text-center"),
                        dcc.Graph(id="barchart_pm", figure=FIG_INIT)
                    ])
                ])
            ])
        ], md=6),
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardHeader("Secondary market"),
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        html.Label(id="lineplot_sm_label",
                                   children="Secondary market prices plot",
                                   className="text-center"),
                        dcc.Graph(id="lineplot_sm", figure=FIG_INIT)
                    ]),
                    dbc.Row(children=[
                        html.Label(id="barchart_sm_label",
                                   children="Secondary market mean quarterly geometric return chart",
                                   className="text-center"),
                        dcc.Graph(id="barchart_sm", figure=FIG_INIT)
                    ])
                ])
            ])
        ], md=6)
    ], align="center"),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardHeader("Indices"),
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        dbc.Col(children=[
                            dbc.Label("Select index"),
                            dcc.Dropdown(
                                id="dropdown_index",
                                options=INDICES,
                                multi=False,
                                searchable=False,
                                placeholder="Index..."
                            )]
                        )]
                    ),
                    dbc.Row(children=[
                        dbc.Col(children=[
                            dbc.Label("Select index weighting"),
                            dcc.Dropdown(
                                id="dropdown_index_weighting",
                                options=INDEX_TYPES,
                                multi=False,
                                searchable=False,
                                placeholder="Index weighting..."
                            )]
                        )]
                    )
                ])
            ])
        ], md=4),
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        html.Label(id="chart_indices_label",
                                   children="Real estate market indices",
                                   className="text-center"),
                        dcc.Graph(id="chart_indices", figure=FIG_INIT)
                    ])
                ])
            ])
        ], md=8)
    ]),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardHeader("Derivations"),
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        dbc.Col(children=[
                            dbc.Label("Select price series"),
                            dcc.Dropdown(
                                id="dropdown_combi",
                                options=[{"label": c, "value": c} for c in COMBINED],
                                multi=True,
                                searchable=True,
                                placeholder="Select price series..."
                            )]
                        )]
                    ),
                    dbc.Row(children=[
                        dbc.Col(children=[
                            dbc.Label("Select category"),
                            dcc.Dropdown(
                                id="dropdown_category",
                                options=CATEGORY,
                                multi=False,
                                searchable=True,
                                placeholder="Select category..."
                            )]
                        )]
                    ),
                    dbc.Row(children=[
                        dbc.Col(children=[
                            dbc.Label("Select feature"),
                            dcc.Dropdown(
                                id="dropdown_feature",
                                options=[],
                                multi=False,
                                searchable=True,
                                placeholder="Select feature..."
                            )]
                        )]
                    )
                ])
            ])
        ], md=4),
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        html.Label(id="chart_feature_label",
                                   children="Selected feature chart",
                                   className="text-center"),
                        dcc.Graph(id="chart_feature", figure=FIG_INIT)
                    ])
                ])
            ])
        ], md=8)
    ]),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardHeader("Association of price levels and quarterly returns"),
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        dbc.Col(children=[
                            dbc.Label("Select X"),
                            dcc.Dropdown(
                                id="dropdown_independent_variable",
                                options=[{'label': c, 'value': c} for c in COMBINED],
                                multi=False,
                                searchable=True,
                                placeholder="Independent variable..."
                            )]
                        )]
                    ),
                    dbc.Row(children=[
                        dbc.Col(children=[
                            dbc.Label("Select Y"),
                            dcc.Dropdown(
                                id="dropdown_dependent_variable",
                                options=[{'label': c, 'value': c} for c in COMBINED],
                                multi=False,
                                searchable=True,
                                placeholder="Dependent variable..."
                            )]
                        )]
                    )
                ])
            ])
        ], md=4),
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        dbc.Label(id="scatter_plot_label",
                                  children="Association of price levels",
                                  className="text-center"),
                        dcc.Graph(id="scatter_plot", figure=FIG_INIT)
                    ])
                ])
            ])
        ], md=4),
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        dbc.Label(id="scatter_plot_ret_label",
                                  children="Association of price changes",
                                  className="text-center"),
                        dcc.Graph(id="scatter_plot_ret", figure=FIG_INIT)
                    ])
                ])
            ])
        ], md=4
        )]
    )],
    id="mainContainer",
    fluid=True
)


@app.callback(
    Output('dropdown_multi_city', 'value'),
    Input('radio_cities', 'value'))
def update_city_dropdown(radio_select):
    if not radio_select:
        raise PreventUpdate
    else:
        if radio_select == "all":
            values = [c for c in CITIES]
        else:
            values = []
    return values


@app.callback(
    [Output('lineplot_pm', 'figure'),
     Output('lineplot_sm', 'figure'),
     Output('barchart_pm', 'figure'),
     Output('barchart_sm', 'figure'),
     Output("lineplot_pm_label", "children"),
     Output("lineplot_sm_label", "children"),
     Output("barchart_pm_label", "children"),
     Output("barchart_sm_label", "children")],
    [Input('checklist_price_a', 'value'),
     Input('radio_price_b', 'value'),
     Input('radio_plot', 'value'),
     Input('dropdown_multi_city', 'value'),
     Input('slider', 'value')]
)
def update_main_figures(offer_vs_trx, prx_type, plot_type, city_scope, time_range):
    if not offer_vs_trx or not prx_type or not plot_type or not city_scope:
        raise PreventUpdate
    else:
        fig_lineplot_pm = create_lineplot("pm", offer_vs_trx, prx_type, plot_type, city_scope, time_range)
        fig_lineplot_sm = create_lineplot("sm", offer_vs_trx, prx_type, plot_type, city_scope, time_range)
        fig_barchart_pm = create_barchart("pm", offer_vs_trx, prx_type, plot_type, city_scope, time_range)
        fig_barchart_sm = create_barchart("sm", offer_vs_trx, prx_type, plot_type, city_scope, time_range)

        label_lineplot_pm = get_lineplot_title(
            "pm",
            offer_vs_trx,
            prx_type,
            plot_type,
            SLIDER_DATE_RANGE[time_range[0]],
            SLIDER_DATE_RANGE[time_range[-1]]
        )
        label_lineplot_sm = get_lineplot_title(
            "sm",
            offer_vs_trx,
            prx_type,
            plot_type,
            SLIDER_DATE_RANGE[time_range[0]],
            SLIDER_DATE_RANGE[time_range[-1]]
        )
        label_barchart_pm = get_barchart_title(time_range, "pm", offer_vs_trx, prx_type)
        label_barchart_sm = get_barchart_title(time_range, "sm", offer_vs_trx, prx_type)

    return fig_lineplot_pm, fig_lineplot_sm, fig_barchart_pm, fig_barchart_sm, label_lineplot_pm, label_lineplot_sm, \
        label_barchart_pm, label_barchart_sm


@app.callback(
    Output("chart_indices", "figure"),
    [Input("dropdown_index", "value"),
     Input("dropdown_index_weighting", "value"),
     Input("dropdown_index_weighting", "label")]
)
def update_index_chart(index_type, index_weighting, index_weighting_label):
    if not index_type or not index_weighting:
        raise PreventUpdate
    else:
        fig = create_index_chart(index_type, index_weighting, index_weighting_label)

    return fig


@app.callback(
    Output("dropdown_feature", "options"),
    Input("dropdown_category", "value")
)
def update_feature_dropdown(category):
    if not category:
        raise PreventUpdate
    else:
        if category == "ret":
            options = [dict(label="Quarterly returns", value="quarterly_ret"),
                       dict(label="Annual returns", value="annual_ret"),
                       dict(label="Rolling annual return", value="roll_annual_ret")]
        elif category == "sentiment":
            options = [dict(label="Positive/negative quarters", value="ud_q"),
                       dict(label="Rolling 1y positive/negative quarters", value="rolling_ud_q"),
                       dict(label="Positive/negative quarters balance", value="ud_q_balance")]
        else:
            options = [dict(label="Rolling annual volatility", value="annual_vol")]

    return options


@app.callback(
    Output("chart_feature", "figure"),
    [Input("dropdown_combi", "value"),
     Input("dropdown_category", "value"),
     Input("dropdown_feature", "value")]
)
def update_feature_chart(combi, cat, feat):
    if not combi or not cat or not feat:
        raise PreventUpdate
    else:
        inputs = combi_breakdown(combi)
        fig = create_feature_chart(inputs, cat, feat)

    return fig


@app.callback(
    [Output("scatter_plot", "figure"),
     Output("scatter_plot_ret", "figure")],
    [Input("dropdown_independent_variable", "value"),
     Input("dropdown_dependent_variable", "value")]
)
def update_scatter_plot(independent_var, dependent_var):
    if not independent_var or not dependent_var:
        raise PreventUpdate
    else:
        ind_inputs = combi_breakdown([independent_var])
        dep_inputs = combi_breakdown([dependent_var])

    fig_prices = create_scatter_plot(ind_inputs, dep_inputs)
    fig_returns = create_scatter_plot(ind_inputs, dep_inputs, True)

    return fig_prices, fig_returns


if __name__ == "__main__":
    app.run_server()
