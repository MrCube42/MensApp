#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Food(object):
    """description of class"""
    
    def __init__(self, name, description, price):
        self.__Name = name
        self.__Description = description
        self.__Price = price
        self.__Starters = []
        self.__Mains = []
        self.__FirstSides = []
        self.__SecondSides = []
        self.__Desserts = []

    def GetName(self):
        return self.__Name

    def GetDescription(self):
        return self.__Description

    def GetPrice(self):
        return self.__Price

    def AddStarter(self, starter):
        self.__Starters.append(starter)

    def AddMain(self, main):
        self.__Mains.append(main)

    def AddFirstSide(self, side):
        self.__FirstSides.append(side)

    def AddSecondSide(self, side):
        self.__SecondSides.append(side)

    def AddDessert(self, dessert):
        self.__Desserts.append(dessert)

    def GetStudentPrice(self):
        return self.__Price.GetStudentPrice()

    def GetStarters(self):
        return self.__Starters

    def GetMains(self):
        return self.__Mains

    def GetFirstSides(self):
        return self.__FirstSides

    def GetSecondSides(self):
        return self.__SecondSides

    def GetDesserts(self):
        return self.__Desserts