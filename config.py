import os
CURRENT_SEASON = 2016
DOMAIN = 'http://www.oddsportal.com'
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
PHANTOM_DRIVER = 'C:\\phantomjs.exe'
CHROME_DRIVER = 'C:\\chromedriver.exe'
SOCCER_COUNTRIES = {'england': ['premier-league', 'championship'],
                    'france': ['ligue-1'],
                    'germany': ['bundesliga', '2-bundesliga'],
                    'italy': ['serie-a'],
                    'spain': ['primera-division'],
                    'netherlands': ['eredivisie'],
                    }
ENGLAND_PATH = os.path.join('soccer', 'england', 'premier-league')
ENGLAND_PARAMS = {'f_min': 3.2, 'f_max': 3.5,
                  'place': 'all', 'extremum': 'max'}
ENGLAND2_PATH = os.path.join('soccer', 'england', 'championship')

NETHERLANDS_PATH = os.path.join('soccer', 'netherlands', 'eredivisie')

FRANCE_PATH = os.path.join('soccer', 'france', 'ligue-1')
FRANCE_PARAMS = {'f_min': 1.8, 'f_max': 2.6,
                  'place': 'all', 'extremum': 'min'}

GERMANY_PATH = os.path.join('soccer', 'germany', 'bundesliga')
GERMANY2_PATH = os.path.join('soccer', 'germany', '2-bundesliga')

ITALY_PATH = os.path.join('soccer', 'italy', 'serie-a')
ITALY_PARAMS = {'f_min': 1.8, 'f_max': 2.2,
                  'place': 'all', 'extremum': 'min'}

SPAIN_PATH = os.path.join('soccer', 'spain', 'primera-division')
SPAIN_PARAMS = {'f_min': 3.5, 'f_max': 5.3,
                  'place': 'away', 'extremum': 'max'}

RUSSIA_PATH = os.path.join('soccer', 'russia', 'premier-league')
SCOTLAND_PATH = os.path.join('soccer', 'scotland', 'premiership')

PATHS_LIST = [ENGLAND_PATH, ENGLAND2_PATH, NETHERLANDS_PATH, FRANCE_PATH,
              GERMANY_PATH, GERMANY2_PATH, ITALY_PATH, SPAIN_PATH,
              RUSSIA_PATH, SCOTLAND_PATH]

def results_url(country, league, page, year='', base_url=DOMAIN,
                sport='soccer'):
    if not year or year == CURRENT_SEASON:
        league_year = league
    else:
        year = '-'.join(['', str(year), str(year + 1)])
        league_year = league + year
    return '/'.join([base_url, sport, country, league_year, 'results/#',
                     'page', str(page)])
