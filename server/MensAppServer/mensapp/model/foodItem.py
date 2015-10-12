#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FoodItem(object):
    """description of class"""

    def __init__(self, name):
        self.__Name = name

    def __str__(self):
        return self.__Name

    def GetName(self):
        return self.__Name