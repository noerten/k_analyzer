CURRENT_SEASON = 2016
DOMAIN = 'http://www.oddsportal.com'
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
PHANTOM_DRIVER = 'C:\\phantomjs.exe'
CHROME_DRIVER = 'C:\\chromedriver.exe'
SOCCER_COUNTRIES = {'england': ['premier-league', 'championship'],
                    'france': ['ligue-1'],
                    'germany': ['bundesliga'],
                    'italy': ['serie-a'],
                    'spain': ['primera-division'],
                    'netherlands': ['eredivisie'],
                    }

print(USER_AGENT)


def results_url(country, league, page, year='', base_url=DOMAIN,
                sport='soccer'):
    if not year or year == CURRENT_SEASON:
        league_year = league
    else:
        year = '-'.join(['', str(year), str(year + 1)])
        league_year = league + year
    return '/'.join([base_url, sport, country, league_year, 'results/#',
                     'page', str(page)])
