#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from mensapp.globals.constants import Constants

class LegacyConverter(object):
    """description of class"""

    __LEGACY_MENSA_DATE_KEY = "date"
    __LEGACY_MENSA_ID_KEY = "mensaId"
    __LEGACY_MENSA_FOODS_KEY = "foods"
    __LEGACY_MENSA_OPEN_HOURS_KEY = "openHours"

    __OR_CONNECT_STRING = " oder "
    __AND_CONNECT_STRING = ", "

    def __init__(self, mensaId, startDate, endDate, mensas, openHours = None):
        self.__Mensas = mensas

        jsonObject = {}
        jsonObject[self.__LEGACY_MENSA_DATE_KEY] = self.__GetFormattedLegacyDateString(startDate, endDate)
        jsonObject[self.__LEGACY_MENSA_ID_KEY] = mensaId
        jsonObject[self.__LEGACY_MENSA_FOODS_KEY] = self.__GetJsonFoods()
        jsonObject[self.__LEGACY_MENSA_OPEN_HOURS_KEY] = self.__GetTemporaryOpenHours()
        self.__JsonObject = jsonObject

    def __GetFormattedLegacyDateString(self, startDate, endDate):
        startDateString = startDate.strftime(Constants.SWTDateFormat)
        endDateString = endDate.strftime(Constants.SWTDateFormat)
        return u"{0}-{1}".format(startDateString, endDateString)

    def GetJsonString(self):
        # make sure that no ascii is returned
        return json.dumps(self.__JsonObject, ensure_ascii = False, sort_keys = True, indent = 1)

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
            price = food.GetStudentPrice()
            if len(price) > 0:
                self.__AppendToOutput(u"<div class='price'>{0}</div>".format(price))
                self.__AppendToOutput("<div class='reference'/>")
            self.__HandleMeals(food.GetStarters())
            self.__HandleMeals(food.GetMains())
            self.__HandleSides(food.GetFirstSides(), food.GetSecondSides())
            self.__HandleMeals(food.GetDesserts())
        self.__AppendToOutput("</div>")

    def __HandleClosedMenu(self):
        self.__AppendToOutput("<div class='menu'><div class='price noprice'>-1</div><div class='reference noprice'/><div class='meal'><b>geschlossen</b></div></div>")

    def __HandleMeals(self, meals):
        self.__AppendToOutput("<div class='meal' "+ self.__GetInlineSpacingAroundMeal() + ">")
        for meal in meals:
            self.__AppendToOutput(u"{0}{1}".format(meal.GetName(), self.__OR_CONNECT_STRING))
        if len(meals) > 0:
            self.__RemoveFromOutputEnd(self.__OR_CONNECT_STRING)
        self.__AppendToOutput("</div>")

    def __HandleSides(self, firstSides, secondSides):
        self.__AppendToOutput("<div class='meal' "+ self.__GetInlineSpacingAroundMeal() +">")
        for side in firstSides:
            self.__AppendToOutput(u"{0}{1}".format(side.GetName(), self.__OR_CONNECT_STRING))
        if len(firstSides) > 0:
            self.__RemoveFromOutputEnd(self.__OR_CONNECT_STRING)
        if len(firstSides) > 0 and len(secondSides) > 0:
            self.__AppendToOutput(self.__AND_CONNECT_STRING)
        for side in secondSides:
            self.__AppendToOutput(u"{0}{1}".format(side.GetName(), self.__OR_CONNECT_STRING))
        if len(secondSides) > 0:
            self.__RemoveFromOutputEnd(self.__OR_CONNECT_STRING)
        self.__AppendToOutput("</div>")

    def __AppendToOutput(self, content):
        self.__Output = self.__Output + content

    def __RemoveFromOutputEnd(self, contentToRemove):
        self.__Output = self.__Output[:-len(contentToRemove)]

    def __GetInlineSpacingAroundMeal(self):
        # Spacing in html is currently to narrow -> adjust this with a transparent border
        return "style='border-width: 3px; border-style: solid; border-color: transparent;'"

    # This is just a workaround because the current OpenHours are not available yet
    def __GetTemporaryOpenHours(self):
        return "<div class='openHoursNormal'><div>Momentan leider nicht verfügbar.</div>"