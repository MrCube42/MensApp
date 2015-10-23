#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mensapp.model.mensa import Mensa
from mensapp.model.menu import Menu
from mensapp.model.food import Food
from mensapp.model.foodItem import FoodItem
from mensapp.model.price import Price

from mensapp.globals.constants import Constants
import datetime

import json

# TODO!
class HtmlConverter(object):
    """description of class"""

    __OrConnectString = " oder "
    __AndConnectString = ", "

    def __init__(self, startDate, endDate, mensaId, mensas, openHours = None):
        startDateString = startDate.strftime(Constants.SWTDateFormat)
        endDateString = endDate.strftime(Constants.SWTDateFormat)
        self.__DateString = u"{0}-{1}".format(startDateString, endDateString)
        self.__MensaId = mensaId
        self.__OpenHours = openHours
        self.__Mensas = mensas

    def GetJsonString(self):
        jsonObject = {}
        jsonObject["date"] = self.__DateString
        jsonObject["mensaId"] = self.__MensaId
        jsonObject["foods"] = self.__GetJsonFoods()
        jsonObject["openHours"] = self.__GetOpenHours()
        # do make sure that unicode is used instead of ascii
        return json.dumps(jsonObject, ensure_ascii = False)

    def __GetJsonFoods(self):
        foods = []
        for mensa in self.__Mensas:
            menus = []
            for menu in mensa.GetMenus():
                if(menu.HasFood()):
                    menus.append(self.__ConvertMenu(menu))
            foods.append("".join(menus))
        return foods

    def __ConvertMenu(self, menu):
        self.__Output = ""

        self.__AppendToOutput(u"<div class='theke'>{0}</div>".format(menu.GetName()))

        if menu.IsOpen():
            self.__HandleOpenedMenu(menu)
        else:
            self.__HandleClosedMenu()
        
        return self.__Output

    def __HandleOpenedMenu(self, menu):
        self.__AppendToOutput("<div class='menu'>")
        for food in menu.GetFoods():
            self.__AppendToOutput(u"<div class='price'>{0}</div>".format(food.GetStudentPrice()))
            self.__AppendToOutput("<div class='reference'/>")
            self.__HandleMeals(food.GetStarters())
            self.__HandleMeals(food.GetMains())
            self.__HandleSides(food.GetFirstSides(), food.GetSecondSides())
            self.__HandleMeals(food.GetDesserts())
        self.__AppendToOutput("</div>")

    def __HandleClosedMenu(self):
        self.__AppendToOutput("<div class='menu'><div class='price noprice'>-1</div><div class='reference noprice'/><div class='meal'><b>geschlossen</b></div></div>")

    def __HandleMeals(self, meals):
        self.__AppendToOutput("<div class='meal'>")
        for meal in meals:
            self.__AppendToOutput(u"{0}{1}".format(meal.GetName(), self.__OrConnectString))
        if len(meals) > 0:
            self.__RemoveFromOutputEnd(self.__OrConnectString)
        self.__AppendToOutput("</div>")

    def __HandleSides(self, firstSides, secondSides):
        self.__AppendToOutput("<div class='meal'>")

        for side in firstSides:
            self.__AppendToOutput(u"{0}{1}".format(side.GetName(), self.__OrConnectString))
        if len(firstSides) > 0:
            self.__RemoveFromOutputEnd(self.__OrConnectString)

        if len(firstSides) > 0 and len(secondSides) > 0:
            self.__AppendToOutput(self.__AndConnectString)

        for side in secondSides:
            self.__AppendToOutput(u"{0}{1}".format(side.GetName(), self.__OrConnectString))
        if len(secondSides) > 0:
            self.__RemoveFromOutputEnd(self.__OrConnectString)

        self.__AppendToOutput("</div>")

    def __AppendToOutput(self, content):
        self.__Output = self.__Output + content

    def __RemoveFromOutputEnd(self, contentToRemove):
        self.__Output = self.__Output[:-len(contentToRemove)]

    def __GetOpenHours(self):
        return "<div class='openHoursNormal'><div>Momentan leider nicht verfügbar.</div>"