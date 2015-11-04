#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mensapp.model.mensa import Mensa
from mensapp.model.menu import Menu

class Test_Mensa(unittest.TestCase):

    def test_GetName(self):
        expectedName = "FooBar"
        mensa = Mensa(4711, expectedName)
        self.assertEqual(expectedName, mensa.GetName())

    def test_GetId(self):
        exptectedId = 42
        mensa = Mensa(exptectedId)
        self.assertEqual(exptectedId, mensa.GetId())

    def test_IsOpenDefault(self):
        mensa = Mensa(123, "MyName")
        self.assertTrue(mensa.IsOpen())

    def test_IsOpenTrue(self):
        mensa = Mensa(123, "MyName", True)
        self.assertTrue(mensa.IsOpen())

    def test_IsOpenFalse(self):
        mensa = Mensa(123, "MyName", False)
        self.assertFalse(mensa.IsOpen())

    def test_HasMenusFalse(self):
        mensa = Mensa(None)
        self.assertFalse(mensa.HasMenus())

    def test_HasMenusTrue(self):
        menu = Menu("A single menu")
        mensa = Mensa(None)
        mensa.AddMenu(menu)
        self.assertTrue(mensa.HasMenus())

    def test_SingleMenu(self):
        menu = Menu("FirstMenu")
        expectedMenus = [menu]
        mensa = Mensa(None)
        mensa.AddMenu(menu)
        self.assertEqual(expectedMenus, mensa.GetMenus())

    def test_MultipleMenus(self):
        menu1 = Menu("FirstMenu")
        menu2 = Menu("SecondMenu")
        expectedMenus = [menu1, menu2]
        mensa = Mensa(None)
        mensa.AddMenu(menu1)
        mensa.AddMenu(menu2)
        self.assertEqual(expectedMenus, mensa.GetMenus())