#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mensapp.model.foodItem import FoodItem

class Test_FoodItem(unittest.TestCase):

    def test_GetName(self):
        expectedName = "FooBar"
        foodItem = FoodItem(expectedName)
        self.assertEqual(expectedName, foodItem.GetName())

    def test_GetNameNone(self):
        foodItem = FoodItem(None)
        self.assertIsNone(foodItem.GetName())