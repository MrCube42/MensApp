#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Mensa(object):
    """description of class"""

    def __init__(self, id, name = None, isOpen = True):
        self.__Id = id
        self.__Name = name
        self.__IsOpen = isOpen
        self.__Menus = []

    def GetId(self):
        return self.__Id

    def GetName(self):
        return self.__Name

    def IsOpen(self):
        return self.__IsOpen

    def AddMenu(self, menu):
        self.__Menus.append(menu)

    def GetMenus(self):
        return self.__Menus

    def HasMenus(self):
        return len(self.__Menus) > 0