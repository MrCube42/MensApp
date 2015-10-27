#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FoodItem(object):
    """description of class"""

    def __init__(self, name):
        self.__Name = name

    def GetName(self):
        return self.__Name