#!/usr/bin/env python
# encoding: utf-8

import unittest
from bridgelib import constants


class TestConstants(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(constants.PLAYERS, ['N', 'E', 'S', 'W'])
        self.assertEqual(constants.PLAYERS_COUNT, 4)
        self.assertEqual(constants.CARD_COLORS, ['s', 'h', 'd', 'c'])
        self.assertEqual(constants.CARD_VALUES, ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'])
        self.assertEqual(constants.ALL_CARDS_COUNT, 52)
        self.assertEqual(constants.HAND_CARDS_COUNT, 13)
        self.assertEqual(constants.BID_COLORS, ['c', 'd', 'h', 's', 'nt'])
        self.assertEqual(constants.BID_VALUES, ['1', '2', '3', '4', '5', '6', '7'])
        self.assertEqual(constants.SPECIAL_BIDS, ["pass", "dbl", "rdbl"])
        self.assertEqual(constants.ALL_BIDS_COUNT, 38)
