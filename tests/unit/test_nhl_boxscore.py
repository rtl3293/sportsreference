from flexmock import flexmock
from mock import patch, PropertyMock
from sportsreference import utils
from sportsreference.constants import AWAY, HOME
from sportsreference.nhl.boxscore import Boxscore


class MockName:
    def __init__(self, name):
        self._name = name

    def text(self):
        return self._name


def mock_pyquery(url):
    class MockPQ:
        def __init__(self, html_contents):
            self.status_code = 404
            self.html_contents = html_contents
            self.text = html_contents

    boxscore = read_file('%s.html' % BOXSCORE)
    return MockPQ(boxscore)


class TestNHLBoxscore:
    @patch('requests.get', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        flexmock(Boxscore) \
            .should_receive('_parse_game_data') \
            .and_return(None)

        self.boxscore = Boxscore(None)

    def test_away_team_wins(self):
        fake_away_goals = PropertyMock(return_value=4)
        fake_home_goals = PropertyMock(return_value=3)
        type(self.boxscore)._away_goals = fake_away_goals
        type(self.boxscore)._home_goals = fake_home_goals

        assert self.boxscore.winner == AWAY

    def test_home_team_wins(self):
        fake_away_goals = PropertyMock(return_value=3)
        fake_home_goals = PropertyMock(return_value=4)
        type(self.boxscore)._away_goals = fake_away_goals
        type(self.boxscore)._home_goals = fake_home_goals

        assert self.boxscore.winner == HOME

    def test_winning_name_is_home(self):
        expected_name = 'Home Name'

        fake_winner = PropertyMock(return_value=HOME)
        fake_home_name = PropertyMock(return_value=MockName(expected_name))
        type(self.boxscore).winner = fake_winner
        type(self.boxscore)._home_name = fake_home_name

        assert self.boxscore.winning_name == expected_name

    def test_winning_name_is_away(self):
        expected_name = 'Away Name'

        fake_winner = PropertyMock(return_value=AWAY)
        fake_away_name = PropertyMock(return_value=MockName(expected_name))
        type(self.boxscore).winner = fake_winner
        type(self.boxscore)._away_name = fake_away_name

        assert self.boxscore.winning_name == expected_name

    def test_winning_abbr_is_home(self):
        expected_name = 'HOME'

        flexmock(utils) \
            .should_receive('_parse_abbreviation') \
            .and_return(expected_name)

        fake_winner = PropertyMock(return_value=HOME)
        fake_home_abbr = PropertyMock(return_value=MockName(expected_name))
        type(self.boxscore).winner = fake_winner
        type(self.boxscore)._home_abbr = fake_home_abbr

        assert self.boxscore.winning_abbr == expected_name

    def test_winning_abbr_is_away(self):
        expected_name = 'AWAY'

        flexmock(utils) \
            .should_receive('_parse_abbreviation') \
            .and_return(expected_name)

        fake_winner = PropertyMock(return_value=AWAY)
        fake_away_abbr = PropertyMock(return_value=MockName(expected_name))
        type(self.boxscore).winner = fake_winner
        type(self.boxscore)._away_abbr = fake_away_abbr

        assert self.boxscore.winning_abbr == expected_name

    def test_losing_name_is_home(self):
        expected_name = 'Home Name'

        fake_winner = PropertyMock(return_value=AWAY)
        fake_home_name = PropertyMock(return_value=MockName(expected_name))
        type(self.boxscore).winner = fake_winner
        type(self.boxscore)._home_name = fake_home_name

        assert self.boxscore.losing_name == expected_name

    def test_losing_name_is_away(self):
        expected_name = 'Away Name'

        fake_winner = PropertyMock(return_value=HOME)
        fake_away_name = PropertyMock(return_value=MockName(expected_name))
        type(self.boxscore).winner = fake_winner
        type(self.boxscore)._away_name = fake_away_name

        assert self.boxscore.losing_name == expected_name

    def test_losing_abbr_is_home(self):
        expected_name = 'HOME'

        flexmock(utils) \
            .should_receive('_parse_abbreviation') \
            .and_return(expected_name)

        fake_winner = PropertyMock(return_value=AWAY)
        fake_home_abbr = PropertyMock(return_value=MockName(expected_name))
        type(self.boxscore).winner = fake_winner
        type(self.boxscore)._home_abbr = fake_home_abbr

        assert self.boxscore.losing_abbr == expected_name

    def test_losing_abbr_is_away(self):
        expected_name = 'AWAY'

        flexmock(utils) \
            .should_receive('_parse_abbreviation') \
            .and_return(expected_name)

        fake_winner = PropertyMock(return_value=HOME)
        fake_away_abbr = PropertyMock(return_value=MockName(expected_name))
        type(self.boxscore).winner = fake_winner
        type(self.boxscore)._away_abbr = fake_away_abbr

        assert self.boxscore.losing_abbr == expected_name

    def test_invalid_away_game_winning_goals_returns_default(self):
        goals = ['0', '1', 'bad']

        fake_goals = PropertyMock(return_value=goals)
        fake_num_skaters = PropertyMock(return_value=3)
        type(self.boxscore)._away_game_winning_goals = fake_goals
        type(self.boxscore)._away_skaters = fake_num_skaters

        assert self.boxscore.away_game_winning_goals == 1

    def test_invalid_away_even_strength_assists_returns_default(self):
        assists = ['0', '1', 'bad']

        fake_assists = PropertyMock(return_value=assists)
        fake_num_skaters = PropertyMock(return_value=3)
        type(self.boxscore)._away_even_strength_assists = fake_assists
        type(self.boxscore)._away_skaters = fake_num_skaters

        assert self.boxscore.away_even_strength_assists == 1

    def test_invalid_home_even_strength_assists_returns_default(self):
        assists = ['0', '1', 'bad']

        fake_assists = PropertyMock(return_value=assists)
        fake_num_skaters = PropertyMock(return_value=0)
        type(self.boxscore)._home_even_strength_assists = fake_assists
        type(self.boxscore)._away_skaters = fake_num_skaters

        assert self.boxscore.home_even_strength_assists == 1

    def test_invalid_away_power_play_assists_returns_default(self):
        assists = ['0', '1', 'bad']

        fake_assists = PropertyMock(return_value=assists)
        fake_num_skaters = PropertyMock(return_value=3)
        type(self.boxscore)._away_power_play_assists = fake_assists
        type(self.boxscore)._away_skaters = fake_num_skaters

        assert self.boxscore.away_power_play_assists == 1

    def test_invalid_home_power_play_assits_returns_default(self):
        assists = ['0', '1', 'bad']

        fake_assists = PropertyMock(return_value=assists)
        fake_num_skaters = PropertyMock(return_value=0)
        type(self.boxscore)._home_power_play_assists = fake_assists
        type(self.boxscore)._away_skaters = fake_num_skaters

        assert self.boxscore.home_power_play_assists == 1

    def test_invalid_away_short_handed_assists_returns_default(self):
        assists = ['0', '1', 'bad']

        fake_assists = PropertyMock(return_value=assists)
        fake_num_skaters = PropertyMock(return_value=3)
        type(self.boxscore)._away_short_handed_assists = fake_assists
        type(self.boxscore)._away_skaters = fake_num_skaters

        assert self.boxscore.away_short_handed_assists == 1

    def test_invalid_home_short_handed_assits_returns_default(self):
        assists = ['0', '1', 'bad']

        fake_assists = PropertyMock(return_value=assists)
        fake_num_skaters = PropertyMock(return_value=0)
        type(self.boxscore)._home_short_handed_assists = fake_assists
        type(self.boxscore)._away_skaters = fake_num_skaters

        assert self.boxscore.home_short_handed_assists == 1

    def test_invalid_url_returns_none(self):
        result = Boxscore(None)._retrieve_html_page('')

        assert result is None
