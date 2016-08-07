ESPN Basketball
===============

**Warning**: This is a very outdated project. I would recommend you look to build
your scrapers with something like [Scrapy](http://scrapy.org) instead.


About
-----

As a huge fan of both basketball and BeautifulSoup 4 (currently in alpha), I
decided to rewrite an earlier module I'd been using to scrape games from ESPN.
In order to use this package, you will need `lxml`, `mock`, and `bs4`
installed.

I've found it parses pages and data pretty fast &mdash; around a second to
parse a game, rearrange the data into a tuple, and then spit it back out. On
average, most games normally consist of 400 to 460 individual plays (timeouts
and interruptions are counted as an Offical Play).

The tuple returned consists of the away team, home team, and a list of
dictionaries (each one represents an individual play in the game). You can
always read the source code to find out more.

Also, the library does have numerous unit tests that you can check out.


Usage
-----

Using the datetime module.

    >>> import datetime
    >>> from espn import get_games
    >>> yesterday = datetime.date.today() - datetime.timedelta(1)
    >>> for game in get_games(yesterday, iterable=True):
    ...     print game

Alternatively you can just use a string in `YYYYMMDD` format.

    >>> yesterday_string = "20110330"
    >>> for game in get_games(yesterday_string, iterable=True):
    ...     print game

You don't have to use the `iterable=True` argument &mdash; a list will be passed
back to you.

    >>> april_fools_last_year = "20100401"
    >>> games = get_games(april_fools_last_year)

You can also scrape NCAA Men's Basketball games by passing in a
`league='ncb'` argument.

    >>> march_1 = '20110301'
    >>> for ncb_game in get_games(march_1, league='ncb', iterable=True):
    ...     print ncb_game

The `daterange` function can also come in handy for generating days between two
specific dates.

    >>> import datetime
    >>> from espn import daterange, get_games
    >>> yesterday = datetime.date.today() - datetime.timedelta(1)
    >>> week_ago = yesterday - datetime.timedelta(7)
    >>> for day in daterange(week_ago, yesterday):
    ...     for game in get_games(day):
    ...         print game
