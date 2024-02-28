import unittest
from unittest import TestCase
from unittest.mock import patch

import exchange_rate

class TestExchangeRate(TestCase):

    @patch('exchange_rates.request_rates')
    def test_dollars_to_target(self, mock_rates):
        mock_rate = 14.1414
        example_api_response = {"rates":{"CAD":mock_rate},"base":"USD","date":"2020-10-02"}
        mock_rates.side_effect = [ example_api_response ]
        converted = exchange_rate.convert_dollars_to_target(100, 'CAD')
        expected = 1414.14
        self.assertEqual(expected, converted)
        

