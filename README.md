ESPN Basketball
===============


About
-----

As a huge fan of both basketball and BeautifulSoup 4 (currently in alpha), I
decided to rewrite an earlier module I'd been using to scrape games from ESPN.
In order to use this package, you will need both lxml and bs4 installed.

I've found it parses pages and data pretty fast &mdash; around a second to
parse a game, rearrange the data into a tuple, and then spit it back out. On
average, most games normally consist of 400 to 450 individual plays (timeouts
and interruptions are counted as an Offical Play).

The tuple returned consists of the away team, home team, and a list of
dictionaries (each on represents an individual play in the game). You can
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

    >>> april_fools_last_year = "20110401"
    >>> games = get_games(april_fools_last_year)
