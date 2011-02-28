from BeautifulSoup import BeautifulSoup as bs
from BeautifulSoup import SoupStrainer
import urllib2
import re
import time
import datetime
from urlparse import urlparse


def daterange(start, end):
    """Generator for days between two specific days."""
    for n in range((end - start).days):
        yield start + datetime.timedelta(n)

def scrape_links(day, league='nba'):
    """Let's scrape ESPN's scoreboard for Play-By-Play links."""
    link = league.lower() + '/scoreboard?date='
    if isinstance(day, datetime.date):
        link += day.strftime('%Y%m%d')
    else:
        link += day
    if league is 'ncb':
        link += '&confId=50'
    scores = 'http://scores.espn.go.com/' + link
    url = urllib2.urlopen(scores)
    print url.geturl()

    content = SoupStrainer('div', {'class': 'span-4'})
    soup = bs(url.read(), parseOnlyThese=content)

    links = (a['href'] for a in soup.findAll('a') if re.match('Play.*',
        a.contents[0]))
    queries = [urlparse(link).query for link in links]
    return queries

def adjust_game(plays):
    """
    Takes plays from parse_plays (generator of lists) and returns
    a list of plays in dictionary format -- which is more
    convenient for lookups.

    The dictionary contains the following information: quarter, quarter_time,
    overall_time, home_score, away_score, home_play, away_play, and 
    official_play (for timeouts, starts of quarters, etc).
    """
    # NOTE: Can't use new_play['quarter'] for NCB games. They use halves.
    # Maybe 'period' instead of 'quarter'?
    game = []
    quarter = 1
    end_of_quarter = False
    for play in plays:
        new_play = _play_as_dict(play)
        quarter_time = play[0]
        time_dict, quarter, end_of_quarter = _adjust_time(quarter_time,
                quarter, end_of_quarter)
        new_play.update(time_dict)
        try:
            scores = play[2]
        except IndexError:
            if len(game) > 0:
                last_play = game[-1]
                new_play['away_score'] = last_play['away_score']
                new_play['home_score'] = last_play['home_score']
            else:
                new_play['away_score'] = 0
                new_play['home_score'] = 0
        else:
            away_score, home_score = scores.split('-')
            new_play['away_score'] = int(away_score)
            new_play['home_score'] = int(home_score)
        game.append(new_play)
    return game

def _adjust_time(quarter_time, quarter, end_of_quarter):
    """
    Takes the time logic out of adjust_game.
    Returns a dict, quarter, and end_of_quarter.
    """
    time = re.split(':', quarter_time)
    minute = int(time[0])
    seconds = int(time[1])
    if minute is 0 and not end_of_quarter:
        end_of_quarter = True
    elif end_of_quarter and minute > 1:
        quarter += 1
        end_of_quarter = False
    if quarter > 4:
        quarter_length = 5
    else:
        quarter_length = 12
    mins = datetime.timedelta(minutes=quarter_length) -\
            datetime.timedelta(minutes=minute, seconds=seconds)
    overall_time = str(mins +
            datetime.timedelta(minutes=(12 * (quarter - 1))))
    time_dict = {}
    time_dict['overall_time'] = overall_time
    time_dict['quarter_time'] = quarter_time
    time_dict['quarter'] = quarter
    return time_dict, quarter, end_of_quarter

def _play_as_dict(play):
    """
    Give it a play in list/tuple format, get back a dict containing
    official_play, home_play, and away_play data.

    Really only for internal use with adjust_game.
    """
    new_play = {}
    if len(play) is 2:
        new_play['official_play'] = play[1]
        new_play['home_play'] = None
        new_play['away_play'] = None
    else:
        new_play['official_play'] = None
        away_play = play[1]
        home_play = play[3]
        if away_play == '&nbsp;':
            new_play['away_play'] = None
            new_play['home_play'] = home_play
        elif home_play == '&nbsp;':
            new_play['away_play'] = away_play
            new_play['home_play'] = None
    return new_play

def parse_plays(game, league='nba'):
    """Parse a game's Play-By-Play page on ESPN."""
    espn = 'http://scores.espn.go.com/' + league + '/playbyplay?' +\
            game + '&period=0'
    url = urllib2.urlopen(espn)
    print url.geturl()

    content = SoupStrainer('table', {'class': 'mod-data'})
    soup = bs(url.read(), parseOnlyThese=content)
    thead = [thead.extract() for thead in soup.findAll('thead')] 
    rows = (list(tr(text=True)) for tr in soup.findAll('tr'))
    game = adjust_game(rows)
    print len(game)
    teams = thead[0].findChildren('th', {'width':'40%'})
    return game

def get_games(day, json=False, league='nba'):
    """
    Get the games and play-by-play data from ESPN for a date.
    The date can be in datetime.date format or be a YYYYMMDD string.

    By default it only looks for NBA games on a date. You can modify
    this by passing it a league='ncb' argument to scrape the NCAA men's
    basketball games that have Play-By-Play data.
    """
    all_games = scrape_links(day, league=league)
    for game in all_games[:2]:
        info = parse_plays(game, league=league)
        if json:
            import json
            print json.dumps(info)
        else:
            print info

def main():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    get_games(yesterday)

if __name__ == '__main__':
    start = time.time()
    main()
    print time.time() - start, 'seconds'
