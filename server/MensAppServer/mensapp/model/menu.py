#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Menu(object):
    """description of class"""

    def __init__(self, name, isOpen = True):
        self.__Name = name
        self.__IsOpen = isOpen
        self.__Foods = []

        # TODO: Do we need this?
    #def __str__(self):
    #    stringRepresentation = self.__Name
    #    if not self.IsOpen():
    #        stringRepresentation = stringRepresentation + " (geschlossen)"
    #    return stringRepresentation

    def AddFood(self, food):
        self.__Foods.append(food)

    def GetName(self):
        return self.__Name

    def GetFoods(self):
        return self.__Foods

    def IsOpen(self):
        return self.__IsOpen

    def HasFood(self):
        return len(self.__Foods) > 0