#!/usr/bin/env python

"""Unit tests for `espn.py` file."""

import unittest
import datetime
from espn import (daterange, _format_scoreboard_url, scrape_links, adjust_game,
        _league_time, _calc_overall_time, _play_as_dict, _adjust_time)


class DateRangeTest(unittest.TestCase):

    def test_week_has_gone_by(self):
        now = datetime.date(2010, 2, 27)
        week_ago = now - datetime.timedelta(days=7)
        days = [day for day in daterange(week_ago, now)]
        self.assertEqual(len(days), 7)


class FormatScoreboardUrlTest(unittest.TestCase):

    def setUp(self):
        self.date = datetime.date(2010, 2, 26)
        self.date_string = '20100226'
        self.correct_nba_link = ('http://scores.espn.go.com/nba/scoreboard?'
                'date=20100226')
        self.correct_ncb_link = ('http://scores.espn.go.com/ncb/scoreboard?'
                'date=20100226&confId=50')

    def test_format_nba_link_with_datetime(self):
        self.assertEqual(_format_scoreboard_url(self.date),
                self.correct_nba_link)

    def test_format_nba_link_with_date_string(self):
        self.assertEqual(_format_scoreboard_url(self.date_string),
                self.correct_nba_link)

    def test_format_ncb_link_with_datetime(self):
        self.assertEqual(_format_scoreboard_url(self.date, league='ncb'),
                self.correct_ncb_link)

    def test_format_ncb_link_with_date_string(self):
        self.assertEqual(_format_scoreboard_url(self.date_string,
                league='ncb'), self.correct_ncb_link)

    def test_format_link_with_capital_case(self):
        self.assertEqual(_format_scoreboard_url(self.date, league='NBA'),
                self.correct_nba_link)

    def test_format_link_with_mixed_case(self):
        self.assertEqual(_format_scoreboard_url(self.date, league='NbA'),
                self.correct_nba_link)


class ScrapeLinksTest(unittest.TestCase):

    def setUp(self):
        self.link = 'http://scores.espn.go.com/nba/scoreboard?date=20100226'
        self.games = [u'gameId=300226001', u'gameId=300226028',
                      u'gameId=300226025', u'gameId=300226010',
                      u'gameId=300226021', u'gameId=300226023',
                      u'gameId=300226027', u'gameId=300226004',
                      u'gameId=300226029', u'gameId=300226007',
                      u'gameId=300226003', u'gameId=300226013']

    def test_scrape_links(self):
        self.assertEqual(scrape_links(self.link), self.games)


class AdjustTimeTest(unittest.TestCase):

    def setUp(self):
        self.adjusted = _adjust_time('12:00', 1, True, 'nba')

    def test_dictionary_output(self):
        time = self.adjusted[0]
        self.assertEqual(time, {'quarter': 2, 'quarter_time': '12:00',
            'overall_time': '0:12:00'})

    def test_quarter_increases(self):
        quarter = self.adjusted[1]
        self.assertEqual(quarter, 2)

    def test_end_of_quarter_becomes_false(self):
        end_of_quarter = self.adjusted[2]
        self.assertEqual(end_of_quarter, False)

    def test_end_of_quarter_becomes_true(self):
        new_adjusted = _adjust_time('0:55', 1, False, 'nba')
        end_of_quarter = new_adjusted[2]
        self.assertEqual(end_of_quarter, True)


class LeagueTimeTest(unittest.TestCase):

    def test_nba_league_time(self):
        num_quarters, regulation_time, regular_quarter = _league_time('nba')
        self.assertEqual(num_quarters, 4)
        self.assertEqual(regulation_time, 48)
        self.assertEqual(regular_quarter, 12)

    def test_ncb_league_time(self):
        num_quarters, regulation_time, regular_quarter = _league_time('ncb')
        self.assertEqual(num_quarters, 2)
        self.assertEqual(regulation_time, 40)
        self.assertEqual(regular_quarter, 20)


class CalcOverallTimeTest(unittest.TestCase):

    def test_beginning_of_game_nba(self):
        time = _calc_overall_time(0, 12, 1, 'nba')
        self.assertEqual(time, '0:00:00')

    def test_beginning_of_second_quarter_nba(self):
        time = _calc_overall_time(0, 12, 2, 'nba')
        self.assertEqual(time, '0:12:00')

    def test_five_minutes_into_third_quarter_nba(self):
        time = _calc_overall_time(0, 7, 3, 'nba')
        self.assertEqual(time, '0:29:00')

    def test_last_five_minutes_of_fourth_quarter_nba(self):
        time = _calc_overall_time(0, 5, 4, 'nba')
        self.assertEqual(time, '0:43:00')

    def test_last_minute_of_overtime_nba(self):
        time = _calc_overall_time(0, 1, 5, 'nba')
        self.assertEqual(time, '0:52:00')

    def test_beginning_of_triple_overtime_nba(self):
        time = _calc_overall_time(0, 5, 7, 'nba')
        self.assertEqual(time, '0:58:00')

    def test_beginning_of_game_ncb(self):
        time = _calc_overall_time(0, 20, 1, 'ncb')
        self.assertEqual(time, '0:00:00')

    def test_five_minutes_into_first_half_ncb(self):
        time = _calc_overall_time(0, 15, 1, 'ncb')
        self.assertEqual(time, '0:05:00')

    def test_beginning_of_second_half_ncb(self):
        time = _calc_overall_time(0, 20, 2, 'ncb')
        self.assertEqual(time, '0:20:00')

    def test_ten_minutes_into_second_half_ncb(self):
        time = _calc_overall_time(0, 10, 2, 'ncb')
        self.assertEqual(time, '0:30:00')

    def test_beginning_of_overtime_ncb(self):
        time = _calc_overall_time(0, 5, 3, 'ncb')
        self.assertEqual(time, '0:40:00')

    def test_last_minute_of_second_overtime_ncb(self):
        time = _calc_overall_time(0, 1, 4, 'ncb')
        self.assertEqual(time, '0:49:00')

    def test_beginning_of_third_overtime_ncb(self):
        time = _calc_overall_time(0, 5, 5, 'ncb')
        self.assertEqual(time, '0:50:00')


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


class AdjustGameTest(unittest.TestCase):

    def setUp(self):
        self.game = [['12:00', 'Start of Game'],
                     ['6:00', 'Away team scores!', '2-0', '&nbsp;'],
                     ['0:01', '&nbsp;', '2-2', 'Home team scores!'],
                     ['12:00', 'Start of new quarter']]

    def test_away_play_equals_none(self):
        plays = [['2:00', '&nbsp;', '0-0', 'Home team play!']]
        adjusted_play = adjust_game(plays)[0]
        self.assertEqual(adjusted_play['away_play'], None)

    def test_home_play_equals_none(self):
        plays = [['2:00', 'Away team play!', '0-0', '&nbsp;']]
        adjusted_play = adjust_game(plays)[0]
        self.assertEqual(adjusted_play['home_play'], None)

    def test_last_play_has_home_score(self):
        adjusted_game = adjust_game(self.game)
        last_play = adjusted_game[-1]
        self.assertTrue(last_play['home_score'])
        self.assertEqual(last_play['home_score'], 2)

    def test_last_play_has_away_score(self):
        adjusted_game = adjust_game(self.game)
        last_play = adjusted_game[-1]
        self.assertTrue(last_play['away_score'])
        self.assertEqual(last_play['away_score'], 2)

    def test_last_play_quarter_equals_2(self):
        adjusted_game = adjust_game(self.game)
        last_play = adjusted_game[-1]
        self.assertEqual(last_play['quarter'], 2)

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
        self.assertEqual(adjust_game(self.game),
                expected_output)


if __name__ == '__main__':
    unittest.main()
