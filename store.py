city_store = ['Białystok', 'Bydgoszcz', 'Gdańsk', 'Gdynia', 'Katowice', 'Kielce', 'Kraków', 'Lublin', 'Łódź', 'Olsztyn',
              'Poznań', 'Rzeszów', 'Szczecin', 'Warszawa', 'Wrocław']

line_colors_store = {
    'Bydgoszcz': 'rgb(189, 189, 189)',
    'Białystok': 'rgb(255, 204, 251)',
    'Olsztyn': 'rgb(128, 201, 0)',
    'Kielce': 'rgb(77, 255, 231)',
    'Szczecin': 'rgb(191, 2, 65)',
    'Wrocław': 'rgb(125, 255, 253)',
    'Warszawa': 'rgb(244, 255, 117)',
    'Kraków': 'rgb(233, 153, 255)',
    'Lublin': 'rgb(235, 255, 0)',
    'Poznań': 'rgb(105, 130, 255)',
    'Łódź': 'rgb(122, 200, 255)',
    'Gdynia': 'rgb(255, 255, 255)',
    'Gdańsk': 'rgb(255, 117, 117)',
    'Katowice': 'rgb(160, 255, 158)',
    'Rzeszów': 'rgb(133, 65, 67)'
}

table_cols = ['1 year', '2 years', '3 years', '5 years', '10 years',
              'Annualized quarterly arithmetic mean return', 'Annualized quarterly geometric mean return',
              'Annualized quarterly median return', 'Best quarter', 'Worst quarter', '# Positive quarters',
              '# Negative quarters', '# Positive quarters in last 3 years', '# Negative quarters in last 3 years',
              'Longest streak of positive quarters', 'Longest streak of negative quarters', 'Annual volatility',
              'Annual upside volatility', 'Annual downside volatility', 'Sharpe ratio', 'Sortino ratio',
              'Best 1 year rolling return', 'Best 2 year rolling return', 'Best 3 year rolling return',
              'Best 5 year rolling return', 'Best 10 year rolling return', 'Worst 1 year rolling return',
              'Worst 2 year rolling return', 'Worst 3 year rolling return', 'Worst 5 year rolling return',
              'Worst 10 year rolling return', 'Correlation with large cap stocks', 'Large cap correlation p-value',
              'Correlation with mid cap stocks', 'Mid cap correlation p-value', 'Correlation with small cap stocks',
              'Small cap correlation p-value', 'Real Estate sector correlation', 'Sector correlation p-value',
              'Return vs large cap stocks', 'Return vs mid cap stocks', 'Return vs small cap stocks',
              'Return vs sector stocks']

analytics_var_store = {'pm_op_ret': 'Primary market offer prices quarterly change',
                       'pm_tp_ret': 'Primary market transaction prices quarterly change',
                       'sm_op_ret': 'Secondary market offer prices quarterly change',
                       'sm_tp_ret': 'Secondary market transaction prices quarterly change',
                       'pm_spread': 'Primary market offer-transaction prices spread',
                       'sm_spread': 'Secondary market offer-transaction prices spread',
                       'op_spread': 'Primary-secondary market offer prices spread',
                       'tp_spread': 'Primary-secondary market transaction prices spread',
                       'pm_tp_vol_one': 'Primary market transaction prices 1-year rolling volatility',
                       'pm_tp_vol_five': 'Primary market transaction prices 5-year rolling volatility',
                       'sm_tp_vol_one': 'Secondary market transaction prices 1-year rolling volatility',
                       'sm_tp_vol_five': 'Secondary market transaction prices 5-year rolling volatility'}

style_header = {'padding': '10px', 'fontWeight': 'bold', 'border': '2px solid white'}

style_cell = {'whiteSpace': 'normal', 'backgroundColor': '#001540', 'color': 'white', 'maxWidth': '400px',
              'minWidth': '150px', 'fontSize': '14pt'}

style_cell_conditional = [{'if': {'column_id': 'City'}, 'textAlign': 'left'}]

label_hist_ret = 'Historical rates of return across multiple time horizons'

label_hist_mean = 'Past return averages and historical max/min quarterly returns'

label_trend = 'Up/down trend statistics'

label_vol = 'Historical volatility and risk-adjusted return measures'

label_roll_1 = 'Highest historical rolling returns'

label_roll_2 = 'Lowest historical rolling returns'

label_corr_1 = 'Correlation with equity market indices 1/2'

label_corr_2 = 'Correlation with equity market indices 2/2'

label_perf = 'Performance vs equity market indices'
