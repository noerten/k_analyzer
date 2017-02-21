import os
import pprint

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

from pickle_io import load_pickle

matplotlib.style.use('ggplot')


def set_filtered_coef_pos(row):
    if row['filtered_coef'] == row['home_coef']:
        return 0
    elif row['filtered_coef'] == row['away_coef']:
        return 2
    else:
        return 1


def count_profit(row, bet_profit=50, stype='profit', better_price_k=1.00):
    """Returns profit for row, depending on stype. If stype == 'bet',
     bet amount is always the same and equals to bet_profit.
     If stype == 'profit', bet amount varies, so than profit amount would
     always be the same and equal to bet_profit. Also better_price_k can be
     implemented in order to describe result using better coefs
     then oddsportal average"""

    if stype == 'bet':
        bet = bet_profit
        if row['filtered_coef_pos'] == row['result']:
            return (row['filtered_coef'] * better_price_k - 1) * bet
        else:
            return -bet
    if stype == 'profit':
        profit = bet_profit
        # removed  coef from getting bet size
        bet = profit / (row['filtered_coef'] - 1)
        if row['filtered_coef_pos'] == row['result']:
            return (row['filtered_coef'] * better_price_k - 1) * bet
        else:
            return -bet


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


def study_france(df, f_min=1.8, f_max=2.6, place='all'):
    # away лучше?
    df['filtered_coef'] = df[['home_coef', 'draw_coef', 'away_coef']].min(axis=1)
    df = df.loc[df['filtered_coef'] > f_min]
    df = df.loc[df['filtered_coef'] < f_max]
    if place == 'all':
        pass
    elif place == 'home':
        df = df.loc[df['filtered_coef'] == df['home_coef']]
    elif place == 'away':
        df = df.loc[df['filtered_coef'] == df['away_coef']]
    elif place == 'draw':
        df = df.loc[df['filtered_coef'] == df['draw_coef']]
    else:
        raise ValueError
    df['filtered_coef_pos'] = df.apply(set_filtered_coef_pos, axis=1)
    df = df.reset_index()
    df['profit'] = df.apply(count_profit, axis=1, better_price_k=1.00)
    df['profit1.02'] = df.apply(count_profit, axis=1, better_price_k=1.02)
    df['profit1.03'] = df.apply(count_profit, axis=1, better_price_k=1.03)
    df['profit1.04'] = df.apply(count_profit, axis=1, better_price_k=1.04)
    print(df)
    df_sum = df['profit'].sum()
    return df, df_sum


def study_england(df, f_min=3.2, f_max=3.50, place='all'):
    # f_min=3.2, f_max=3.5, place = 'all') 500 6700 стремительныйрост во второй половине
    # f_min=4.8, f_max=8.5, place = 'all') soso
    df['filtered_coef'] = df[['home_coef', 'draw_coef', 'away_coef']].max(axis=1)
    df = df.loc[df['filtered_coef'] > f_min]
    df = df.loc[df['filtered_coef'] < f_max]
    if place == 'all':
        pass
    elif place == 'home':
        df = df.loc[df['filtered_coef'] == df['home_coef']]
    elif place == 'away':
        df = df.loc[df['filtered_coef'] == df['away_coef']]
    elif place == 'draw':
        df = df.loc[df['filtered_coef'] == df['draw_coef']]
    else:
        raise ValueError
    df['filtered_coef_pos'] = df.apply(set_filtered_coef_pos, axis=1)
    df = df.reset_index()
    df['profit'] = df.apply(count_profit, axis=1, better_price_k=1.00)
    df['profit1.02'] = df.apply(count_profit, axis=1, better_price_k=1.02)
    df['profit1.03'] = df.apply(count_profit, axis=1, better_price_k=1.03)
    df['profit1.04'] = df.apply(count_profit, axis=1, better_price_k=1.04)

    df_sum = df['profit'].sum()
    return df, df_sum


def study_germany(df, f_min=3.4, f_max=3.5, place='draw', extremum='max'):
    # nothing worth mentioing
    if extremum == 'max':
        df['filtered_coef'] = df[['home_coef', 'draw_coef', 'away_coef']].max(axis=1)
    elif extremum == 'min':
        df['filtered_coef'] = df[['home_coef', 'draw_coef', 'away_coef']].min(axis=1)
    df = df.loc[df['filtered_coef'] > f_min]
    df = df.loc[df['filtered_coef'] < f_max]
    if place == 'all':
        pass
    elif place == 'home':
        df = df.loc[df['filtered_coef'] == df['home_coef']]
    elif place == 'away':
        df = df.loc[df['filtered_coef'] == df['away_coef']]
    elif place == 'draw':
        df = df.loc[df['filtered_coef'] == df['draw_coef']]
    else:
        raise ValueError
    df['filtered_coef_pos'] = df.apply(set_filtered_coef_pos, axis=1)
    df = df.reset_index()
    df['profit'] = df.apply(count_profit, axis=1, better_price_k=1.00)
    df['profit1.02'] = df.apply(count_profit, axis=1, better_price_k=1.02)
    df['profit1.03'] = df.apply(count_profit, axis=1, better_price_k=1.03)
    df['profit1.04'] = df.apply(count_profit, axis=1, better_price_k=1.04)

    df_sum = df['profit'].sum()
    return df, df_sum


def study_spain(df, f_min=3.5, f_max=5.3, place='away', extremum='max'):
    #  f_min=3.5, f_max=5.3, place = 'away', extremum = 'max')
    # nothing worth mentioing
    if extremum == 'max':
        df['filtered_coef'] = df[['home_coef', 'draw_coef', 'away_coef']].max(axis=1)
    elif extremum == 'min':
        df['filtered_coef'] = df[['home_coef', 'draw_coef', 'away_coef']].min(axis=1)
    df = df.loc[df['filtered_coef'] > f_min]
    df = df.loc[df['filtered_coef'] < f_max]
    if place == 'all':
        pass
    elif place == 'home':
        df = df.loc[df['filtered_coef'] == df['home_coef']]
    elif place == 'away':
        df = df.loc[df['filtered_coef'] == df['away_coef']]
    elif place == 'draw':
        df = df.loc[df['filtered_coef'] == df['draw_coef']]
    else:
        raise ValueError
    df['filtered_coef_pos'] = df.apply(set_filtered_coef_pos, axis=1)
    df = df.reset_index()
    df['profit'] = df.apply(count_profit, axis=1, better_price_k=1.00)
    df['profit1.02'] = df.apply(count_profit, axis=1, better_price_k=1.02)
    df['profit1.03'] = df.apply(count_profit, axis=1, better_price_k=1.03)
    df['profit1.04'] = df.apply(count_profit, axis=1, better_price_k=1.04)

    df_sum = df['profit'].sum()
    return df, df_sum


def plot_df(df):
    df.drop(['index', 'away_coef', 'draw_coef', 'home_coef', 'result',
             'filtered_coef', 'filtered_coef_pos'], axis=1, inplace=True)
    df.drop('level_0', axis=1, inplace=True)
    #    print(df.describe())
    #    df.set_index('datetime', inplace=True)
    df.drop('datetime', axis=1, inplace=True)
    print(df)
    df = df.cumsum()
    df.plot()
    plt.show()


def brut_force(wrapper_path):
    desired_range = ([x / 10.0 for x in range(14, 40, 1)] +
                     [x / 10.0 for x in range(40, 60, 2)] +
                     [x / 10.0 for x in range(60, 100, 3)] +
                     [x / 10.0 for x in range(100, 200, 10)])
    print(desired_range)
    output = []
    counter = 0
    starting_df = load_league_df(wrapper_path)
    for i in desired_range:
        for j in desired_range:
            for place in ['home', 'away', ' draw', 'all']:
                for extr in ['min', 'max']:
                    counter += 1
                    if counter % 20 == 0:
                        print(counter * 100 / (2 * 4 * len(desired_range) ** 2))
                    df = starting_df
                    try:
                        df = study_spain(df, i, j, place, extremum=extr)
                        if df[1] < 300:
                            continue
                        if len(df[0]) > 500:
                            output.append([df[1], i, j, place, len(df[0]), extr])
                    except:
                        continue

    pprint.pprint(sorted(output))


def analyze():
    epl_path = os.path.join('soccer', 'england', 'premier-league')
    france_path = os.path.join('soccer', 'france', 'ligue-1')
    germany_path = os.path.join('soccer', 'germany', 'bundesliga')
    italy_path = os.path.join('soccer', 'italy', 'serie-a')
    spain_path = os.path.join('soccer', 'spain', 'primera-division')
    england2_path = os.path.join('soccer', 'england', 'championship')
    wrapper_path = england2_path
    #    brut_force(england2_path)
    #    sys.exit()
    df = load_league_df(wrapper_path)
    if wrapper_path == france_path:
        df = study_france(df)[0]
    elif wrapper_path == epl_path:
        df = study_england(df)[0]
    elif wrapper_path == germany_path:
        df = study_germany(df)[0]
    elif wrapper_path == spain_path:
        df = study_spain(df)[0]
    df_e2 = study_spain(df, 3.3, 3.5, place='all', extremum='max')[0]
    df_i = study_spain(df, 1.8, 2.2, place='all', extremum='min')[0]
    # italy soso    df_i = study_spain(df, 2.9, 3.4, place='all', extremum = 'max')[0]

    ## for italy     df_i = study_spain(df, 1.8, 2.2, place='all', extremum = 'min')[0]
    df_e = study_england(load_league_df(epl_path))[0]
    df_f = study_france(load_league_df(france_path))[0]
    df_s = study_spain(load_league_df(spain_path))[0]
    #    df_e2 = study_england(load_league_df(epl_path), f_min=4.8, f_max=8.5)[0]
    #    print(len(df_f))
    #    print(len(df_e2))
    #    result = pd.concat([df, df_f, df_e2])
    #    result = pd.concat([df_e, df_f, df_s, df_i])
    result = df_e2
    #    result = df
    result = result.sort('datetime')
    #    with pd.option_context('display.max_rows', None, 'display.max_columns', 7):
    print(result)
    result = result.reset_index()

    plot_df(result)


if __name__ == '__main__':
    analyze()
