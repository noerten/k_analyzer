import datetime
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import config
from pickle_io import picklize
from pickle_io import save_pickle


def create_folders(countries, sport='soccer'):
    """Create folders for pickle files with annual coefs info"""
    for country in countries:
        for league in countries[country]:
            location = os.path.join(sport, country, league)
            if not os.path.exists(location):
                os.makedirs(location)


def init_web_driver(use_driver='phantom'):
    if use_driver == 'phantom':
        phantom_driver = config.PHANTOM_DRIVER
        caps = DesiredCapabilities.PHANTOMJS
        caps["phantomjs.page.settings.userAgent"] = config.USER_AGENT
        driver = webdriver.PhantomJS(phantom_driver,
                                     desired_capabilities=caps)
    elif use_driver == 'chrome':
        chromedriver = config.CHROME_DRIVER
        driver = webdriver.Chrome(chromedriver)
    else:
        raise ValueError('incorrect web driver')
    return driver


def get_html(url, driver):
    driver.get(url)
    time.sleep(1.5)
    return driver.page_source


def make_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_match_result(score):
    """Returns 0 for home winner, 1 for draw, 2 for away winner"""
    score = score.strip(' ET')
    score_list = score.split(':')
    home_goals = int(score_list[0])
    away_goals = int(score_list[1])
    if home_goals > away_goals:
        return 0
    elif home_goals < away_goals:
        return 2
    else:
        return 1


def get_match_datetime(list_with_attrs):
    """Extracts datetime from html attribute"""
    for attr in list_with_attrs:
        if attr.startswith('t1'):
            match_timestamp = int(attr.split('-', 1)[0].lstrip('t'))
            return datetime.datetime.fromtimestamp(match_timestamp)


def get_page_matches(html):
    """Return list with matches from one page"""
    soup = make_soup(html)
    matches = []
    for row in soup.find(id='tournamentTable').tbody \
            .find_all('tr', class_='deactivate', recursive=False):
        match = {}
        datetime_cell = row.find(class_='table-time')
        match['datetime'] = get_match_datetime(datetime_cell['class'])
        match_cell = row.find(class_='name table-participant')
        teams = match_cell.get_text().strip().split('-')
        match['home_team'] = teams[0].strip()
        match['away_team'] = teams[1].strip()
        other_cells = match_cell.find_next_siblings('td')
        result_str = other_cells[0].get_text()
        if (result_str == 'award.' or result_str == 'postp.' or
            result_str == 'pen.'):
            print(result_str)
            continue
        try:
            match['result'] = get_match_result(result_str)
        except ValueError:
            continue
        match['home_coef'] = other_cells[1].get_text()
        match['draw_coef'] = other_cells[2].get_text()
        match['away_coef'] = other_cells[3].get_text()
        matches.append(match)
    print('len(matches)', len(matches))
    return matches


def get_number_of_pages(html):
    soup = make_soup(html)
    return int(soup.find(id='pagination').find_all('a')[-1]['x-page'])


def get_saved_years(sport_type, country, league):
    file_list = os.listdir(os.path.join(sport_type, country, league))
    return [int(year_file.split('.pickle')[0]) for year_file in file_list]


def get_coefs():
    create_folders(config.SOCCER_COUNTRIES)
    driver = init_web_driver()
    sport_type = 'soccer'
    for country in config.SOCCER_COUNTRIES:
        print('parsing country:', country)
        for league in config.SOCCER_COUNTRIES[country]:
            print('parsing league: ', league)
            for year in range(config.CURRENT_SEASON, 2010, -1):
                if year in get_saved_years(sport_type, country, league):
                    print('year', year, 'was already saved')
                    continue
                year_matches = []
                print('parsing year:', year)
                league_url = config.results_url(country, league, 1, year=year)
                print('getting number of pages from url:', league_url)
                number_of_pages = get_number_of_pages(get_html(league_url,
                                                               driver))
                for page in range(1, number_of_pages + 1):
                    print('parsing page: ', page)
                    page_url = config.results_url(country, league, page,
                                                  year=year)
                    year_matches.extend(get_page_matches(get_html(page_url,
                                                                  driver)))
                save_pickle(year_matches, os.path.join(sport_type, country,
                                                       league, picklize(year)))
                print('saved to pickle')
    driver.close()


if __name__ == '__main__':
    get_coefs()
