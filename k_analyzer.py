import os
import pprint

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

import config
from pickle_io import load_pickle

matplotlib.style.use('ggplot')


def set_filtered_coef_pos(row):
    if row['filtered_coef'] == row['home_coef']:
        return 0
    elif row['filtered_coef'] == row['away_coef']:
        return 2
    else:
        return 1



def count_bet_size(row, bet_profit=50, stype='profit'):
    """Returns bet_size  depending on stype. If stype == 'bet',
     bet amount is always the same and equals to bet_profit.
     If stype == 'profit', bet amount varies, so than profit amount would
     always be the same and equal to bet_profit."""

    if stype == 'bet':
        return bet_profit
    if stype == 'profit':
        profit = bet_profit
        # removed  coef from getting bet size
        return profit / (row['filtered_coef'] - 1)

def count_profit(row, better_price_k=1.00):
    """Returns profit for row, depending on bet_size"""
    if row['filtered_coef_pos'] == row['result']:
        return (row['filtered_coef'] * better_price_k - 1) * row['bet_size']
    else:
        return - row['bet_size']


def save_to_txt(the_list, filepath):
    with open(filepath + '.txt', 'w') as the_file:
        for item in the_list:
            the_file.write("%s\n" % item)


def load_league_df(path):
    matches = []
    for year in sorted(os.listdir(path)):
        matches.extend(list(reversed(load_pickle(os.path.join(path, year)))))
    league_df = pd.DataFrame(matches)
    league_df.drop('away_team', axis=1, inplace=True)
    league_df[['away_coef', 'draw_coef', 'home_coef',
               'result']] = league_df[['away_coef', 'draw_coef', 'home_coef',
                                       'result']].apply(pd.to_numeric)
    league_df = league_df.assign(profit=0)
    return league_df


def get_strategy_result(league_df, f_min=2.0, f_max=4.0, place='all', extremum='max'):
    """Return league dataframe with applied strategy. f_min and f_max define range in
    which use coef, place can be 'home', 'draw', 'away', 'not_draw', 'all'.
    extremum defines what extremum value for filtered coef to use and
     can be either max or min and defines """
    if extremum == 'max':
        league_df['filtered_coef'] = league_df[['home_coef', 'draw_coef',
                                                'away_coef']].max(axis=1)
    elif extremum == 'min':
        league_df['filtered_coef'] = league_df[['home_coef', 'draw_coef',
                                                'away_coef']].min(axis=1)
    league_df = league_df.loc[league_df['filtered_coef'] > f_min]
    league_df = league_df.loc[league_df['filtered_coef'] < f_max]
    if place == 'all':
        pass
    elif place == 'home':
        league_df = league_df.loc[league_df['filtered_coef'] ==
                                  league_df['home_coef']]
    elif place == 'away':
        league_df = league_df.loc[league_df['filtered_coef'] ==
                                  league_df['away_coef']]
    elif place == 'draw':
        league_df = league_df.loc[league_df['filtered_coef'] ==
                                  league_df['draw_coef']]
    elif place == 'notdraw':
        league_df = league_df.loc[league_df['filtered_coef'] ==
                                  league_df['away_coef'] or
                                  league_df['filtered_coef'] ==
                                  league_df['home_coef']]
    else:
        raise ValueError
    league_df['filtered_coef_pos'] = league_df.apply(set_filtered_coef_pos,
                                                     axis=1)
    league_df['bet_size'] = league_df.apply(count_bet_size, axis=1)
    league_df['profit'] = league_df.apply(count_profit, axis=1,
                                          better_price_k=1.00)
    league_df['profit1.02'] = league_df.apply(count_profit, axis=1,
                                              better_price_k=1.02)
    league_df['profit1.03'] = league_df.apply(count_profit, axis=1,
                                              better_price_k=1.03)
    league_df['profit1.04'] = league_df.apply(count_profit, axis=1,
                                              better_price_k=1.04)
    return league_df


def plot_df(df, timeline=False):
    roi = df['profit'].sum()/df['bet_size'].sum()
    roi02 = df['profit1.02'].sum()/df['bet_size'].sum()
    df.drop(['index', 'away_coef', 'draw_coef', 'home_coef', 'result',
             'filtered_coef', 'filtered_coef_pos', 'bet_size'], axis=1,
            inplace=True)
    try:
        df.drop('level_0', axis=1, inplace=True)
    except ValueError:
        pass
    if not timeline:
        df.drop('datetime', axis=1, inplace=True)
    else:
        df.set_index('datetime', inplace=True)
    print(df)
    print(roi)
    print(roi02)
    df = df.cumsum()
    df.plot()
    plt.show()


def show_progress(current, total, decimals=2):
    number = current / total*100
    print('{0:,.{1}f}%'.format(number, decimals))


def find_strategies(league_path):
    desired_range = (
        [x / 10.0 for x in range(10, 40, 10)] +
        [x / 10.0 for x in range(40, 60, 2)] +
        [x / 10.0 for x in range(60, 100, 5)] +
        [x / 10.0 for x in range(100, 200, 10)]
    )
    output = []
    counter = 0
    starting_df = load_league_df(league_path)
    places = ['home', 'away', ' draw', 'all', 'notdraw']
    extremums = ['min', 'max']
    for f_max in desired_range:
        for f_min in desired_range:
            if f_max > f_min:
                for place in places:
                    for extremum in extremums:
                        counter += 1
                        if counter % 20 == 0:
                            show_progress(counter, len(places) * len(extremum)
                                          * 3.33 * len(desired_range) ** 2)
                        try:
                            resulting_df = get_strategy_result(starting_df,
                                                               f_min, f_max,
                                                               place,
                                                               extremum)
                            len_df = len(resulting_df)
                            profit_df = resulting_df['profit'].sum()
                            roi = (profit_df/resulting_df['bet_size'].sum())
                            nice_roi = '{0:,.{1}f}%'.format(roi, 2)
                            nice_profit = '{0:,.{1}f}'.format(profit_df, 2)
                            if profit_df < 300:
                                continue
                            if len_df > 300:
                                output.append([nice_roi, nice_profit, f_min, f_max, place,
                                               len_df, extremum])
                        except:
                            continue
    pprint.pprint(sorted(output))
    save_to_txt(sorted(output), os.path.split(league_path)[-2] + '_' +
                os.path.split(league_path)[-1])


def show_strategy(paths_params, timeline=False):
    result = pd.concat([get_strategy_result(load_league_df(path),
                                            **paths_params[path])
                        for path in paths_params])
    result = result.sort('datetime')
    result = result.reset_index()
    plot_df(result, timeline)


if __name__ == '__main__':
    paths_params_dict = {
        config.ENGLAND_PATH: config.ENGLAND_PARAMS,
        config.FRANCE_PATH: config.FRANCE_PARAMS,
        config.SPAIN_PATH: config.SPAIN_PARAMS,
        config.ITALY_PATH: config.ITALY_PARAMS,
    }
 #   show_strategy(paths_params_dict, timeline=True)
    for path in config.PATHS_LIST:
        find_strategies(path)
