#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mensapp.globals.helpers import Helpers
from datetime import datetime

class Test_FoodItem(unittest.TestCase):

    TEST_DATE_FORMAT = "%Y%m%d"

    def test_GetDatesBetweenIncluding(self):
        startDate = datetime(2042, 11, 7, 0, 0, 0)
        endDate = datetime(2042, 11, 10, 0, 0, 0)
        expectedDates = [startDate, datetime(2042, 11, 8, 0, 0, 0), datetime(2042, 11, 9, 0, 0, 0) ,endDate]
        self.assertEqual(expectedDates, Helpers.GetDatesBetweenIncluding(startDate, endDate))

    def test_GetDatesBetweenIncluding_NothingBetween(self):
        startDate = datetime(2042, 11, 7, 0, 0, 0)
        endDate = datetime(2042, 11, 8, 0, 0, 0)
        expectedDates = [startDate, endDate]
        self.assertEqual(expectedDates, Helpers.GetDatesBetweenIncluding(startDate, endDate))

    def test_GetDatesBetweenIncluding_SingleDate(self):
        date = datetime(2042, 11, 7, 0, 0, 0)
        expectedDates = [date]
        self.assertEqual(expectedDates, Helpers.GetDatesBetweenIncluding(date, date))