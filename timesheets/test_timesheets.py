import unittest
from unittest import TestCase
from unittest.mock import patch, call

import timesheets

class TestTimeSheet(TestCase):

    """ mock input() and force it to return a value"""

    # patch decorator replaces input for a mock input
    # in this case 2 (needs to be in a list)
    @patch('builtins.input', side_effect=['2'])
    def test_get_hours_for_day(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2, hours)

    # need valid input at end of list
    @patch('builtins.input', side_effect=['juice', '', '1juice', 'juice2', '2'])
    def test_get_hours_for_day_non_numeric_rejected(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(2, hours)

    @patch('builtins.input', side_effect=['-1', '-1000000', '20'])
    def test_get_hours_for_day_hours_greater_than_zero(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(20, hours)

    @patch('builtins.input', side_effect=['100', '25', '20'])
    def test_get_hours_for_day_hours_less_than_twentyfour(self, mock_input):
        hours = timesheets.get_hours_for_day('Monday')
        self.assertEqual(20, hours)

    # mocking the print function here
    @patch('builtins.print')
    def test_display_total(self, mock_print):
        timesheets.display_total(123)
        mock_print.assert_called_once_with('Total hours worked: 123')

    # doesn't return anything so no side effect
    @patch('timesheets.alert')
    def test_alert_meet_min_hours_doesnt_meet(self, mock_alert):
        timesheets.alert_not_meet_min_hours(12, 30) # expect an alert
        mock_alert.assert_called_once()

    @patch('timesheets.alert')
    def test_alert_meet_min_hours_does_meet_min(self, mock_alert):
        timesheets.alert_not_meet_min_hours(40, 30) # expect no alert
        mock_alert.assert_not_called()

    # this one relies on the return of another function it calls so create a mock return value
    @patch('timesheets.get_hours_for_day')
    def test_get_hours(self, mock_get_hours):
        mock_hours = [5, 7, 9]
        mock_get_hours.side_effect = mock_hours
        days = ['m', 't', 'w']
        excepted_hours = dict(zip(days, mock_hours)) # zip the key to the value
        hours = timesheets.get_hours(days)
        self.assertEqual(excepted_hours, hours)

    @patch('builtins.print')
    def test_display_hours(self, mock_print):
        
        # arrange
        example = {'M': 4, 'T': 11, 'W': 1.25}
        # call object is a tuple so need to create mock tuples
        excepted_table_calls = [
            call('Day          Hours Worked     '),
            call('M            4                '),
            call('T            11               '),
            call('W            1.25             '),
        ]

        # action
        timesheets.display_hours(example)

        # assert
        mock_print.asset_has_calls(excepted_table_calls)

    def test_total_hours(self):
        example = {'M': 4, 'T': 11, 'W': 1.25}
        total = timesheets.total_hours(example)
        excepted_total = 4 + 11 + 1.25
        self.assertEqual(total, excepted_total)

if __name__ == '__main__':
    unittest.main()


        