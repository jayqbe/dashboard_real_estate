import pandas as pd
import numpy as np
from pathlib import Path


# A function to read file from a relative path
def read_file_to_df(file_name, sheet_name=None, cols_to_use=None):
    p = Path('.')

    if file_name == "ceny_mieszkan":
        file_name = file_name + ".xlsx"
        df = pd.read_excel(p / 'res' / file_name, sheet_name=sheet_name, usecols=cols_to_use, header=1,
                           skiprows=5)
        if df.columns[0].endswith(".1"):
            df.rename(columns={
                df.columns[0]: "Białystok",
                df.columns[1]: "Bydgoszcz",
                df.columns[2]: "Gdańsk",
                df.columns[3]: "Gdynia",
                df.columns[4]: "Katowice",
                df.columns[5]: "Kielce",
                df.columns[6]: "Kraków",
                df.columns[7]: "Lublin",
                df.columns[8]: "Łódź",
                df.columns[9]: "Olsztyn",
                df.columns[10]: "Opole",
                df.columns[11]: "Poznań",
                df.columns[12]: "Rzeszów",
                df.columns[13]: "Szczecin",
                df.columns[14]: "Warszawa",
                df.columns[15]: "Wrocław",
                df.columns[16]: "Zielona Góra"
            }, inplace=True)
    elif file_name == "wig20":
        file_name = file_name + "_q.csv"
        df = pd.read_csv(p / 'res' / file_name, usecols=[1])
    elif file_name == "mwig40":
        file_name = file_name + "_q.csv"
        df = pd.read_csv(p / 'res' / file_name, usecols=[1])
    elif file_name == "swig80":
        file_name = file_name + "_q.csv"
        df = pd.read_csv(p / 'res' / file_name, usecols=[1])
    elif file_name == "wig_budow":
        file_name = file_name + "_q.csv"
        df = pd.read_csv(p / 'res' / file_name, usecols=[1])
    elif file_name == "cpi_pl":
        file_name = file_name + ".csv"
        df = pd.read_csv(p / 'res' / file_name, usecols=[1])

    date_range = pd.date_range(start="2006q3", periods=len(df), freq="q")
    df.set_index(date_range, inplace=True)

    return df


def index_to_start(df_):
    df = df_ / df_.iloc[0] * 100

    return df


def multi_period_ret(period_ret):
    return np.prod(period_ret) - 1


def compute_real_prices(df):
    df_cpi = read_file_to_df('cpi_pl')
    df_cpi = df_cpi.div(100).cumprod()
    df_cpi = index_to_start(df_cpi.loc[df.index]).div(100)
    df_real = df.div(df_cpi.loc[df.index].values)

    return df_real


def compute_return(df):
    if len(df) < 5:
        df_ret = (df.iloc[-1] / df.iloc[0] - 1) * 100
    else:
        df_ret = (np.power(df.iloc[-1] / df.iloc[0], 4 / (len(df) - 1)) - 1) * 100

    return df_ret


def get_lineplot_title(mkt_type, offer_vs_trx, prx_type, chart_type, time_start, time_end):
    title_dict = {'pm': 'Primary', 'sm': 'Secondary', 'op': 'offer', 'tp': 'transaction', 'nom': 'nominal',
                  'real': 'real', 'act': '', 'ind': ' (indexed)'}
    title_template = '%s market %s %s prices%s between %s and %s'

    if len(offer_vs_trx) > 1:
        title = title_template % (
            title_dict[str(mkt_type)], title_dict[str(prx_type)], 'offer and transaction ', title_dict[str(chart_type)],
            'Q{}-{}'.format(time_start.quarter, time_start.year), 'Q{}-{}'.format(time_end.quarter, time_end.year))
    else:
        title = title_template % (
            title_dict[str(mkt_type)], title_dict[str(prx_type)], title_dict[str(offer_vs_trx[0])],
            title_dict[str(chart_type)], 'Q{}-{}'.format(time_start.quarter, time_start.year),
            'Q{}-{}'.format(time_end.quarter, time_end.year))

    return title


def get_barchart_title(time_range, mkt_type, offer_vs_trx, prx_type):
    title_dict = {'pm': 'primary', 'sm': 'secondary', 'op': 'offer', 'tp': 'transaction', 'nom': 'nominal',
                  'real': 'real'}
    title_template = 'Annualized geometric mean growth rate of %s market %s %s ' + 'prices in selected period.'
    title_template_short = 'Unannualized growth rate of %s market %s %s prices in selected period'

    if time_range[-1] - time_range[0] < 5:
        if len(offer_vs_trx) > 1:
            title = title_template_short % (title_dict[str(mkt_type)], title_dict[str(prx_type)],
                                            'offer and transaction ')
        else:
            title = title_template_short % (
                title_dict[str(mkt_type)], title_dict[str(prx_type)], title_dict[str(offer_vs_trx[0])])
    else:
        if len(offer_vs_trx) > 1:
            title = title_template % (title_dict[str(mkt_type)], title_dict[str(prx_type)], 'offer and transaction ')
        else:
            title = title_template % (
                title_dict[str(mkt_type)], title_dict[str(prx_type)], title_dict[str(offer_vs_trx[0])])

    return title


def calculate_streaks(df):
    df_ret = pd.DataFrame(df.div(df.shift(1)).sub(1) > 0)
    df_streak = pd.DataFrame(index=df.columns, columns=['up_streak', 'down_streak'])

    for i in df_streak.index:
        ups = df_ret[i].ne(df_ret[i].shift()).cumsum().loc[df_ret[df_ret[i]].index].value_counts().max()
        downs = df_ret[i].ne(df_ret[i].shift()).cumsum().loc[df_ret[~df_ret[i]].index].value_counts().max()
        df_streak['up_streak'].loc[i] = ups
        df_streak['down_streak'].loc[i] = downs

    return [df_streak.up_streak, df_streak.down_streak]


def calculate_index(df: pd.DataFrame, ind_weighting: str):

    if ind_weighting == "equal_weighted":

        const_number = df.shape[-1]

        weights = [1 / const_number] * const_number

        index_equal = df.pct_change().fillna(0).add(1).cumprod().mul(weights, axis=1).sum(axis=1).mul(1000)

        return index_equal

    elif ind_weighting == "price_weighted":

        df = df.fillna(method="ffill")

        weights = df.div(df.sum(axis=1).values, axis=0).shift().fillna(1 / df.shape[1])

        df_ret = df.pct_change()

        index_price = df_ret.fillna(0).add(1).cumprod().mul(weights, axis=1).sum(axis=1).mul(1000)

        return index_price


def combi_breakdown(combi):
    out = list()
    for item in combi:
        market = " ".join(item.split(" ")[0:2])
        prices = " ".join(item.split(" ")[2:4])
        city = item.split(" ")[-1]
        out.append([market, prices, city])

    return out
