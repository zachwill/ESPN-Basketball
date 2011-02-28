import unittest
import datetime
from espn import (daterange, scrape_links, adjust_game,
        _play_as_dict, _adjust_time)


class DateRangeTest(unittest.TestCase):
    now = datetime.date(2010, 2, 27)
    week_ago = now - datetime.timedelta(days=7)
    pass 


class ScrapeLinksTest(unittest.TestCase):

    def setUp(self):
        self.today = datetime.date(2010, 2, 26)
        self.today_string = '20100226'
        self.games = [u'gameId=300226001', u'gameId=300226028',
                u'gameId=300226025', u'gameId=300226010',
                u'gameId=300226021', u'gameId=300226023',
                u'gameId=300226027', u'gameId=300226004',
                u'gameId=300226029', u'gameId=300226007',
                u'gameId=300226003', u'gameId=300226013']

    def test_scrape_links_with_date(self):
        self.assertEquals(scrape_links(self.today), self.games)

    def test_scrape_links_with_string(self):
        self.assertEquals(scrape_links(self.today_string), self.games)

    def test_scrape_links_for_ncb(self):
        #self.assertTrue(scrape_links(self.today, league='ncb'))
        pass


class PlayAsDictTest(unittest.TestCase):

    def test_start_of_game_play(self):
        start_play = ['6:33', 'Start of Game']
        self.assertEqual(_play_as_dict(start_play),
            {'official_play': 'Start of Game', 'home_play': None,
                'away_play':None})

    def test_home_team_play(self):
        home_play = ['3:44', '&nbsp;', '0-0', 'Test comes through!']
        self.assertEqual(_play_as_dict(home_play),
                {'official_play': None, 'home_play': 'Test comes through!',
                    'away_play': None})

    def test_away_team_play(self):
        away_play = ['2:44', 'Away test wins!', '1-0', '&nbsp;']
        self.assertEqual(_play_as_dict(away_play),
                {'official_play': None, 'home_play': None,
                    'away_play': 'Away test wins!'})


class AdjustTimeTest(unittest.TestCase):

    def test_dictionary_output(self):
        adjusted = _adjust_time('12:00', 1, True)
        time = adjusted[0]
        self.assertEquals(time, {'quarter': 2, 'quarter_time': '12:00',
            'overall_time': '0:12:00'})

    def test_quarter_increases(self):
        adjusted = _adjust_time('12:00', 1, True)
        quarter = adjusted[1]
        self.assertEquals(quarter, 2)

    def test_end_of_quarter_becomes_false(self):
        adjusted = _adjust_time('12:00', 1, True)
        end_of_quarter = adjusted[2]
        self.assertEquals(end_of_quarter, False)

    def test_end_of_quarter_becomes_true(self):
        adjusted = _adjust_time('0:55', 1, False)
        end_of_quarter = adjusted[2]
        self.assertEquals(end_of_quarter, True)


class AdjustGameTest(unittest.TestCase):

    def setUp(self):
        self.game = [['12:00', 'Start of Game'],
            ['6:00', 'Away team scores!', '2-0', '&nbsp;'],
            ['0:01', '&nbsp;', '2-2', 'Home team scores!'],
            ['12:00', 'Start of new quarter']]

    def test_away_play_equals_none(self):
        plays = [['2:00', '&nbsp;', '0-0', 'Home team play!']]
        adjusted_play = adjust_game(plays)[0]
        self.assertEquals(adjusted_play['away_play'], None)

    def test_home_play_equals_none(self):
        plays = [['2:00', 'Away team play!', '0-0', '&nbsp;']]
        adjusted_play = adjust_game(plays)[0]
        self.assertEquals(adjusted_play['home_play'], None)

    def test_last_play_has_home_score(self):
        adjusted_game = adjust_game(self.game)
        last_play = adjusted_game[-1]
        self.assertTrue(last_play['home_score'])
        self.assertEquals(last_play['home_score'], 2)

    def test_last_play_has_away_score(self):
        adjusted_game = adjust_game(self.game)
        last_play = adjusted_game[-1]
        self.assertTrue(last_play['away_score'])
        self.assertEquals(last_play['away_score'], 2)

    def test_last_play_quarter_equals_2(self):
        adjusted_game = adjust_game(self.game)
        last_play = adjusted_game[-1]
        self.assertEquals(last_play['quarter'], 2)

    def test_expected_output(self):
        expected_output = [{'away_score': 0, 'quarter_time': '12:00',
                    'overall_time': '0:00:00', 'away_play': None,
                    'home_play': None, 'official_play': 'Start of Game',
                    'quarter': 1, 'home_score': 0},
                {'away_score': 2, 'quarter_time': '6:00',
                    'overall_time': '0:06:00', 'away_play': 'Away team scores!',
                    'home_play': None, 'official_play': None, 'quarter': 1,
                    'home_score': 0},
                {'away_score': 2, 'quarter_time': '0:01',
                    'overall_time': '0:11:59', 'away_play': None,
                    'home_play': 'Home team scores!', 'official_play': None,
                    'quarter': 1, 'home_score': 2},
                {'away_score': 2, 'quarter_time': '12:00',
                    'overall_time': '0:12:00', 'away_play': None,
                    'home_play': None, 'official_play': 'Start of new quarter',
                    'quarter': 2, 'home_score': 2}]
        self.assertEquals(adjust_game(self.game),
                expected_output)


if __name__ == '__main__':
    unittest.main()
