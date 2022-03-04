import numpy as np
import pandas as pd
import plotly.graph_objects as go
from useful_func import read_file_to_df, index_to_start, compute_real_prices, compute_return, calculate_index
from store import line_colors_store


# Global variables
PRIMARY_MKT_SHEET = 1
SECONDARY_MKT_SHEET = 2
OFFER_COLS = [x for x in range(1, 18)]
TRX_COLS = [x for x in range(24, 41)]

# Load data
df_pm_tp = read_file_to_df("ceny_mieszkan", PRIMARY_MKT_SHEET, TRX_COLS)
df_pm_op = read_file_to_df("ceny_mieszkan", PRIMARY_MKT_SHEET, OFFER_COLS)
df_sm_tp = read_file_to_df("ceny_mieszkan", SECONDARY_MKT_SHEET, TRX_COLS)
df_sm_op = read_file_to_df("ceny_mieszkan", SECONDARY_MKT_SHEET, OFFER_COLS)


def create_lineplot(mkt_type, offer_vs_trx, prx_type, chart_type, city_filter, time_range):
    data = []

    if mkt_type == 'pm':
        if 'tp' in offer_vs_trx:
            df = df_pm_tp.iloc[time_range[0]:(time_range[-1] + 1)][city_filter]
            hover_template = 'Trx price: PLN %{y:.0f}<extra></extra>'
            if prx_type == 'real':
                df = compute_real_prices(df)
            if chart_type == 'ind':
                df = index_to_start(df)
                hover_template = 'Indexed trx price: %{y:.0f}<extra></extra>'
            for c in city_filter:
                trace_1 = go.Scatter(
                    x=['Q{}-{}'.format(x.quarter, x.year) for x in df.index],
                    y=df[c],
                    text=c,
                    hovertemplate='<b>%s</b><br>' % c + hover_template,
                    mode='lines',
                    line=dict(
                        color=line_colors_store[c],
                        width=3)
                )
                data.append(trace_1)
        if 'op' in offer_vs_trx:
            df = df_pm_op.iloc[time_range[0]:(time_range[-1] + 1)][city_filter]
            hover_template = 'Offer price: PLN %{y:.0f}<extra></extra>'
            if prx_type == 'real':
                df = compute_real_prices(df)
            if chart_type == 'ind':
                df = index_to_start(df)
                hover_template = 'Indexed ofr price: %{y:.0f}<extra></extra>'
            for c in city_filter:
                trace_2 = go.Scatter(
                    x=['Q{}-{}'.format(x.quarter, x.year) for x in df.index],
                    y=df[c],
                    name=c,
                    hovertemplate='<b>%s</b><br>' % c + hover_template,
                    mode='lines',
                    line=dict(
                        color=line_colors_store[c],
                        dash='dash')
                )
                data.append(trace_2)
    else:
        if 'tp' in offer_vs_trx:
            df = df_sm_tp.iloc[time_range[0]:(time_range[-1] + 1)][city_filter]
            hover_template = 'Trx price: PLN %{y:.0f}<extra></extra>'
            if prx_type == 'real':
                df = compute_real_prices(df)
            if chart_type == 'ind':
                df = index_to_start(df)
                hover_template = 'Indexed trx price: %{y:.0f}<extra></extra>'
            for c in city_filter:
                trace_1 = go.Scatter(
                    x=['Q{}-{}'.format(x.quarter, x.year) for x in df.index],
                    y=df[c],
                    name=c,
                    hovertemplate='<b>%s</b><br>' % c + hover_template,
                    mode='lines',
                    line=dict(
                        color=line_colors_store[c],
                        width=3)
                )
                data.append(trace_1)
        if 'op' in offer_vs_trx:
            df = df_sm_op.iloc[time_range[0]:(time_range[-1] + 1)][city_filter]
            hover_template = 'Offer price: PLN %{y:.0f}<extra></extra>'
            if prx_type == 'real':
                df = compute_real_prices(df)
            if chart_type == 'ind':
                df = index_to_start(df)
                hover_template = 'Indexed ofr price: %{y:.0f}<extra></extra>'
            for c in city_filter:
                trace_2 = go.Scatter(
                    x=['Q{}-{}'.format(x.quarter, x.year) for x in df.index],
                    y=df[c],
                    name=c,
                    hovertemplate='<b>%s</b><br>' % c + hover_template,
                    mode='lines',
                    line=dict(
                        color=line_colors_store[c],
                        dash='dash')
                )
                data.append(trace_2)

    layout = dict(
        autosize=True,
        height=360,
        margin=dict(t=10, b=0),
        hovermode='closest',
        paper_bgcolor='#001540',
        plot_bgcolor='#001540',
        yaxis=dict(showgrid=False, fixedrange=True),
        xaxis=dict(showgrid=False, nticks=10, fixedrange=True),
        showlegend=False,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="white"
        ),
        transition=dict(duration=400)
    )

    fig = go.Figure(layout=layout, data=data)

    return fig


def create_barchart(mkt_type, offer_vs_trx, prx_type, chart_type, city_filter, time_range):
    data = []
    df_ret_op = pd.DataFrame()
    df_ret_tp = pd.DataFrame()
    layout = dict(
        autosize=True,
        height=360,
        margin=dict(t=10, b=0),
        bargap=0.8,
        paper_bgcolor='#001540',
        plot_bgcolor='#001540',
        showlegend=False,
        xaxis=dict(showgrid=False, fixedrange=True),
        yaxis=dict(showgrid=False, fixedrange=True),
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="white"
        ),
        transition=dict(duration=400)
    )

    if not city_filter or not offer_vs_trx:
        fig = go.Figure(layout=layout, data={})
    else:
        if mkt_type == 'pm':
            if 'op' in offer_vs_trx:
                df = df_pm_op.iloc[time_range[0]:(time_range[-1] + 1)][city_filter]
                if prx_type == 'real':
                    df = compute_real_prices(df)
                if chart_type == 'ind':
                    df = index_to_start(df)
                df_ret_op = compute_return(df)
                trace_1 = go.Bar(
                    x=df_ret_op.values,
                    y=df_ret_op.keys(),
                    hovertemplate='<b>%{y}</b><br>' +
                                  'Price type: offer<br>' +
                                  'Rate: %{x:.2f}%' +
                                  '<extra></extra>',
                    orientation='h',
                    text=np.round(df_ret_op.values, 2),
                    textposition='outside',
                    cliponaxis=False,
                    marker_color='rgb(100, 222, 206)'
                )
                data.append(trace_1)
            if 'tp' in offer_vs_trx:
                df = df_pm_tp.iloc[time_range[0]:(time_range[-1] + 1)][city_filter]
                if prx_type == 'real':
                    df = compute_real_prices(df)
                if chart_type == 'ind':
                    df = index_to_start(df)
                df_ret_tp = compute_return(df)
                trace_2 = go.Bar(
                    x=df_ret_tp.values,
                    y=df_ret_tp.keys(),
                    hovertemplate='<b>%{y}</b><br>' +
                                  'Price type: offer<br>' +
                                  'Rate: %{x:.2f}%' +
                                  '<extra></extra>',
                    orientation='h',
                    text=np.round(df_ret_tp.values, 2),
                    textposition='outside',
                    cliponaxis=False,
                    marker_color='rgb(1, 112, 196)'
                )
                data.append(trace_2)
        else:
            if 'op' in offer_vs_trx:
                df = df_sm_op.iloc[time_range[0]:(time_range[-1] + 1)][city_filter]
                if prx_type == 'real':
                    df = compute_real_prices(df)
                if chart_type == 'ind':
                    df = index_to_start(df)
                df_ret_op = compute_return(df)
                trace_1 = go.Bar(
                    x=df_ret_op.values,
                    y=df_ret_op.keys(),
                    hovertemplate='<b>%{y}</b><br>' +
                                  'Price type: offer<br>' +
                                  'Rate: %{x:.2f}%' +
                                  '<extra></extra>',
                    orientation='h',
                    text=np.round(df_ret_op.values, 2),
                    textposition='outside',
                    cliponaxis=False,
                    marker_color='rgb(100, 222, 206)'
                )
                data.append(trace_1)
            if 'tp' in offer_vs_trx:
                df = df_sm_tp.iloc[time_range[0]:(time_range[-1] + 1)][city_filter]
                if prx_type == 'real':
                    df = compute_real_prices(df)
                if chart_type == 'ind':
                    df = index_to_start(df)
                df_ret_tp = compute_return(df)
                trace_2 = go.Bar(
                    x=df_ret_tp.values,
                    y=df_ret_tp.keys(),
                    hovertemplate='<b>%{y}</b><br>' +
                                  'Price type: offer<br>' +
                                  'Rate: %{x:.2f}%' +
                                  '<extra></extra>',
                    orientation='h',
                    text=np.round(df_ret_tp.values, 2),
                    textposition='outside',
                    cliponaxis=False,
                    marker_color='rgb(1, 112, 196)'
                )
                data.append(trace_2)

        if not df_ret_tp.empty and df_ret_op.empty:
            yaxis_dict = dict(categoryarray=df_ret_tp.sort_values().keys(), categoryorder='array',
                              automargin=True)
            gap = .8 / np.sqrt(len(df_ret_tp))
        elif not df_ret_tp.empty and not df_ret_op.empty:
            yaxis_dict = dict(categoryarray=df_ret_tp.sort_values().keys(), categoryorder='array',
                              automargin=True)
            gap = .8 / len(df_ret_tp)
        else:
            yaxis_dict = dict(categoryarray=df_ret_op.sort_values().keys(), categoryorder='array',
                              automargin=True)
            gap = .8 / len(df_ret_op)

        fig = go.Figure(layout=layout, data=data)
        fig.update_layout(yaxis=yaxis_dict, bargap=gap)

    return fig


def create_index_chart(index_type, index_weighting, index_weighting_label):
    if index_type == "all":
        index = calculate_index(df_pm_tp, index_weighting)

    trace = go.Scatter(
        x=['Q{}-{}'.format(x.quarter, x.year) for x in index.index],
        y=index,
        name=index_weighting_label,
        mode='lines'
    )

    layout = dict(
        autosize=True,
        height=360,
        margin=dict(t=10, b=0),
        hovermode='closest',
        paper_bgcolor='#001540',
        plot_bgcolor='#001540',
        yaxis=dict(showgrid=False, fixedrange=True),
        xaxis=dict(showgrid=False, nticks=10, fixedrange=True),
        showlegend=False,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="white"
        ),
        transition=dict(duration=400)
    )

    fig = go.Figure(layout=layout, data=trace)

    return fig


def create_feature_chart(inputs, cat, feat):
    data = list()
    yaxis_title = ""

    for item in inputs:
        if (item[0] == "Primary market") and (item[1] == "Offer prices"):
            df = df_pm_op[item[2]]
        elif (item[0] == "Primary market") and (item[1] == "Transaction prices"):
            df = df_pm_tp[item[2]]
        elif (item[0] == "Secondary market") and (item[1] == "Offer prices"):
            df = df_sm_op[item[2]]
        else:
            df = df_sm_tp[item[2]]

        df_data = pd.DataFrame()
        if cat == "ret":
            if feat == "quarterly_ret":
                df_data = np.round(df.pct_change() * 100, 2)
                yaxis_title = "Return q/q [%]"
            elif feat == "annual_ret":
                df_data = np.round(df.groupby(by=df.index.year).last().pct_change().dropna() * 100, 2)
                yaxis_title = "Annual return [%]"
            elif feat == "roll_annual_ret":
                df_data = np.round((df.diff(4) / df * 100).dropna(), 2)
                yaxis_title = "Rolling 1 year return [%]"
        elif cat == "sentiment":
            if feat == "ud_q":
                df_data = df.pct_change().apply(lambda x: -1 if x < 0 else 1)
                yaxis_title = "Positive/negative quarter"
            elif feat == "rolling_ud_q":
                df_data = df.pct_change().apply(lambda x: -1 if x < 0 else 1).rolling(4).sum()
                yaxis_title = "1 year rolling sum of positive/negative quarters"
            elif feat == "ud_q_balance":
                df_data = df.pct_change().apply(lambda x: -1 if x < 0 else 1).cumsum()
                yaxis_title = "Cumulative sum of positive/negative quarters"
        elif cat == "risk":
            if feat == "annual_vol":
                df_data = df.pct_change().rolling(4).std().dropna()
                yaxis_title = "Annualized volatility [%]"

        traces = go.Bar(
            x=df_data.keys(),
            y=df_data.values,
            name=df_data.name + " " + item[0] + " " + item[1]
        )
        data.append(traces)

    layout = dict(
        autosize=True,
        margin=dict(l=20, t=20, r=0, b=0),
        bargap=0.33,
        paper_bgcolor='#001540',
        plot_bgcolor='#001540',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=-0.1,
            xanchor="left",
            x=0.01,
            orientation="h"
        ),
        xaxis=dict(showgrid=False, fixedrange=True),
        yaxis=dict(showgrid=True, fixedrange=True, title=yaxis_title),
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="white"
        ),
        transition=dict(duration=400)
    )

    fig = go.Figure(layout=layout, data=data)
    return fig


def create_scatter_plot(ind_inputs, dep_inputs, transform=False):
    ind_inputs = ind_inputs[0]
    if (ind_inputs[0] == "Primary market") and (ind_inputs[1] == "Offer prices"):
        ind_data = df_pm_op[ind_inputs[2]]
    elif (ind_inputs[0] == "Primary market") and (ind_inputs[1] == "Transaction prices"):
        ind_data = df_pm_tp[ind_inputs[2]]
    elif (ind_inputs[0] == "Secondary market") and (ind_inputs[1] == "Offer prices"):
        ind_data = df_sm_op[ind_inputs[2]]
    else:
        ind_data = df_sm_tp[ind_inputs[2]]

    dep_inputs = dep_inputs[0]
    if (dep_inputs[0] == "Primary market") and (dep_inputs[1] == "Offer prices"):
        dep_data = df_pm_op[dep_inputs[2]]
    elif (dep_inputs[0] == "Primary market") and (dep_inputs[1] == "Transaction prices"):
        dep_data = df_pm_tp[dep_inputs[2]]
    elif (dep_inputs[0] == "Secondary market") and (dep_inputs[1] == "Offer prices"):
        dep_data = df_sm_op[dep_inputs[2]]
    else:
        dep_data = df_sm_tp[dep_inputs[2]]

    if transform:
        data = go.Scatter(
            x=np.round(ind_data.pct_change() * 100, 2),
            y=np.round(dep_data.pct_change() * 100, 2),
            mode="markers",
            hovertemplate="X = %{x:.2f}<br>Y = %{y:.2f}",
            name=""
        )
        yaxis_title = "Y values [%]"
        xaxis_title = "X values [%]"
    else:
        data = go.Scatter(
            x=ind_data,
            y=dep_data,
            mode="markers",
            hovertemplate="X = %{x:.0f}<br>Y = %{y:.0f}",
            name=""
        )
        yaxis_title = "Y values [PLN]"
        xaxis_title = "X values [PLN]"

    layout = dict(
        autosize=True,
        height=480,
        margin=dict(l=20, t=50, r=0, b=0),
        paper_bgcolor='#001540',
        plot_bgcolor='#001540',
        yaxis=dict(showgrid=True, fixedrange=True, title=yaxis_title),
        xaxis=dict(showgrid=True, fixedrange=True, title=xaxis_title),
        showlegend=False,
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="white"
        ),
        transition=dict(duration=400)
    )

    fig = go.Figure(layout=layout, data=data)

    return fig
