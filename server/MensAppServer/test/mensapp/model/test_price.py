#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mensapp.model.price import Price

class Test_Price(unittest.TestCase):

    def test_GetStudentPrice(self):
        expectedPrice = "42.0"
        price = Price(expectedPrice, None, None)
        self.assertEqual(expectedPrice, price.GetStudentPrice())

    def test_GetEmployeePrice(self):
        expectedPrice = "47.11"
        price = Price(None, expectedPrice, None)
        self.assertEqual(expectedPrice, price.GetEmployeePrice())

    def test_GetGuestPrice(self):
        expectedPrice = "123.0"
        price = Price(None, None, expectedPrice)
        self.assertEqual(expectedPrice, price.GetGuestPrice())