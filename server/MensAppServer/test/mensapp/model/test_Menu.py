#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mensapp.model.menu import Menu
from mensapp.model.food import Food

class Test_Menu(unittest.TestCase):

    def test_GetName(self):
        expectedName = "FooBar"
        menu = Menu(expectedName)
        self.assertEqual(expectedName, menu.GetName())

    def test_IsOpenDefault(self):
        menu = Menu(None)
        self.assertTrue(menu.IsOpen())

    def test_IsOpenTrue(self):
        menu = Menu(None, True)
        self.assertTrue(menu.IsOpen())

    def test_IsOpenFalse(self):
        menu = Menu(None, False)
        self.assertFalse(menu.IsOpen())

    def test_HasFoodFalse(self):
        menu = Menu(None)
        self.assertFalse(menu.HasFood())

    def test_HasFoodTrue(self):
        food = Food("FooBar", "Something", None)
        menu = Menu(None)
        menu.AddFood(food)
        self.assertTrue(menu.HasFood())

    def test_SingleFood(self):
        food = Food("FooBar", "Something", None)
        expectedFoods = [food]
        menu = Menu(None)
        menu.AddFood(food)
        self.assertEqual(expectedFoods, menu.GetFoods())

    def test_MultipleFoods(self):
        food1 = Food("FooBar", "Something", None)
        food2 = Food("BarFoo", "More than that", None)
        expectedFoods = [food1, food2]
        menu = Menu(None)
        menu.AddFood(food1)
        menu.AddFood(food2)
        self.assertEqual(expectedFoods, menu.GetFoods())