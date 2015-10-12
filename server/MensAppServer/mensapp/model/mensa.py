#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Mensa(object):
    """description of class"""

    def __init__(self, id, name, isOpen = True):
        self.__Id = id
        self.__Name = name
        self.__IsOpen = isOpen
        self.__Menus = []

        # TODO: Do we need this?
    #def __str__(self):
    #    stringRepresentation = self.Name
    #    if not self.IsOpen:
    #        stringRepresentation = stringRepresentation + " (geschlossen)"
    #    return stringRepresentation

    def AddMenu(self, menu):
        self.__Menus.append(menu)

    def GetMenus(self):
        return self.__Menus