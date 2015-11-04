#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from mensapp.model.food import Food
from mensapp.model.price import Price
from mensapp.model.foodItem import FoodItem

class Test_Food(unittest.TestCase):

    def test_GetName(self):
        expectedName = "FooBar"
        food = Food(expectedName, None, None)
        self.assertEqual(expectedName, food.GetName())

    def test_GetDescription(self):
        expectedDescription = "This is something special"
        food = Food(None, expectedDescription, None)
        self.assertEqual(expectedDescription, food.GetDescription())

    def test_GetPrice(self):
        expectedPrice = Price("123", "345", "567")
        food = Food(None, None, expectedPrice)
        self.assertEqual(expectedPrice, food.GetPrice())

    def test_GetStudentPrice(self):
        expectedStudentPrice = "47.88"
        price = Price(expectedStudentPrice, "345", "567")
        food = Food(None, None, price)
        self.assertEqual(expectedStudentPrice, food.GetStudentPrice())

    def test_SingleStarter(self):
        starter = FoodItem("soup")
        expectedStarters = [starter]
        food = Food(None, None, None)
        food.AddStarter(starter)
        self.assertEqual(expectedStarters, food.GetStarters())

    def test_MultipleStarters(self):
        starter1 = FoodItem("soup")
        starter2 = FoodItem("sushi")
        expectedStarters = [starter1, starter2]
        food = Food(None, None, None)
        food.AddStarter(starter1)
        food.AddStarter(starter2)
        self.assertEqual(expectedStarters, food.GetStarters())

    def test_SingleMain(self):
        main = FoodItem("bangers and mash")
        expectedMains = [main]
        food = Food(None, None, None)
        food.AddMain(main)
        self.assertEqual(expectedMains, food.GetMains())

    def test_MultipleMains(self):
        main1 = FoodItem("bangers and mash")
        main2 = FoodItem("haggis")
        expectedMains = [main1, main2]
        food = Food(None, None, None)
        food.AddMain(main1)
        food.AddMain(main2)
        self.assertEqual(expectedMains, food.GetMains())

    def test_SingleFirstSide(self):
        side = FoodItem("spaghetti")
        expectedSides = [side]
        food = Food(None, None, None)
        food.AddFirstSide(side)
        self.assertEqual(expectedSides, food.GetFirstSides())

    def test_MultipleFirstSides(self):
        side1 = FoodItem("spaghetti")
        side2 = FoodItem("potatoes")
        expectedSides = [side1, side2]
        food = Food(None, None, None)
        food.AddFirstSide(side1)
        food.AddFirstSide(side2)
        self.assertEqual(expectedSides, food.GetFirstSides())

    def test_SingleSecondSide(self):
        side = FoodItem("spaghetti")
        expectedSides = [side]
        food = Food(None, None, None)
        food.AddSecondSide(side)
        self.assertEqual(expectedSides, food.GetSecondSides())

    def test_MultipleSecondSides(self):
        side1 = FoodItem("spaghetti")
        side2 = FoodItem("potatoes")
        expectedSides = [side1, side2]
        food = Food(None, None, None)
        food.AddSecondSide(side1)
        food.AddSecondSide(side2)
        self.assertEqual(expectedSides, food.GetSecondSides())

    def test_SingleDessert(self):
        dessert = FoodItem("ice cream")
        expectedDesserts = [dessert]
        food = Food(None, None, None)
        food.AddDessert(dessert)
        self.assertEqual(expectedDesserts, food.GetDesserts())

    def test_MultipleDesserts(self):
        dessert1 = FoodItem("ice cream")
        dessert2 = FoodItem("cookies")
        expectedDesserts = [dessert1, dessert2]
        food = Food(None, None, None)
        food.AddDessert(dessert1)
        food.AddDessert(dessert2)
        self.assertEqual(expectedDesserts, food.GetDesserts())