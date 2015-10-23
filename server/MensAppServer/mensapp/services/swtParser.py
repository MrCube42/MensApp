#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import xml.etree.ElementTree as ET
from mensapp.services.xmlParser import XmlParser
from mensapp.model.mensa import Mensa
from mensapp.model.menu import Menu
from mensapp.model.food import Food
from mensapp.model.price import Price
from mensapp.model.foodItem import FoodItem

from mensapp.globals.constants import Constants
from mensapp.globals.helpers import Helpers

from datetime import date
from datetime import datetime
from datetime import timedelta

import urllib

# TODO: Cleanup
class SWTParser(object):
    """description of class"""

    def __init__(self, mensaId, date):# beginDateString = None, endDateString = None):
        self.__Mensas = {}
        self.__MensaId = mensaId
        self.__MensaIdInternal = u"standort-{0}".format(mensaId)
        self.__Result = ""
        self.__Root = None
        self.__Prepare()
        
        #self.__BeginDate = datetime.strptime(beginDateString, Constants.SWTDateFormat)
        #self.__EndDate = datetime.strptime(endDateString, Constants.SWTDateFormat)
        
        #for date in Helpers.GetDatesBetweenIncluding(self.__BeginDate, self.__EndDate):
        #    self.__Parse(date.strftime(Constants.SWTDateFormat))
        self.__Parse(date.strftime(Constants.SWTDateFormat))

    def __Prepare(self):
        fileObj = urllib.urlopen("http://www.studiwerk.de/export/speiseplan.xml")
        raw = fileObj.read()
        self.__Root = ET.fromstring(raw)

    def __Parse(self, date):
        parser = XmlParser()
        dateNode = parser.FindAttributedNode(self.__Root, "artikel", "date", date)
        
        if dateNode is None:
            return

        mensaNode = parser.FindAttributedNode(dateNode, "standort", "id", self.__MensaIdInternal)
        mensaName = parser.FindNodeValue(mensaNode, "label")
        isOpen = parser.FindNodeValue(mensaNode, "geschlossen") == "0"
        
        mensa = Mensa(self.__MensaId, mensaName, isOpen)

        menuNodes = parser.FindNodes(mensaNode, "theke")
        for menuNode in menuNodes:
            menuName = parser.FindNodeValue(menuNode, "label")
            isOpen = parser.FindNodeValue(menuNode, "geschlossen") == "0"

            menu = Menu(menuName, isOpen)

            foodNodes = parser.FindNodes(menuNode, "mahlzeit")
            for foodNode in foodNodes:
                foodName = parser.FindNodeValue(foodNode, "titel")
                foodDescription = parser.FindNodeValue(foodNode, "beschreibung")

                studentPriceNode = parser.FindAttributedNode(foodNode, "price", "id", "price-1")
                employeePriceNode = parser.FindAttributedNode(foodNode, "price", "id", "price-2")
                guestPriceNode = parser.FindAttributedNode(foodNode, "price", "id", "price-3")
                
                studentPrice = ""
                employeePrice = ""
                guestPrice = ""
                if studentPriceNode is not None:
                    studentPrice = parser.FindNodeAttribute(studentPriceNode, "data")
                if employeePriceNode is not None:
                    employeePrice = parser.FindNodeAttribute(studentPriceNode, "data")
                if guestPriceNode is not None:
                    guestPrice = parser.FindNodeAttribute(studentPriceNode, "data")

                foodPrice = Price(studentPrice, employeePrice, guestPrice)

                food = Food(foodName, foodDescription, foodPrice)

                starterRoot = parser.FindNode(foodNode, "vorspeise")
                starterNodes = parser.FindNodes(starterRoot, "data")
                for starterNode in starterNodes:
                    starterName = parser.FindNodeValue(starterNode, "label")
                    starter = FoodItem(starterName)
                    food.AddStarter(starter)

                mainRoot = parser.FindNode(foodNode, "hauptkomponente")
                mainNodes = parser.FindNodes(mainRoot, "data")
                for mainNode in mainNodes:
                    mainName = parser.FindNodeValue(mainNode, "label")
                    main = FoodItem(mainName)
                    food.AddMain(main)

                sideRoot = parser.FindNode(foodNode, "beilage1")
                sideNodes = parser.FindNodes(sideRoot, "data")
                for sideNode in sideNodes:
                    sideName = parser.FindNodeValue(sideNode, "label")
                    side = FoodItem(sideName)
                    food.AddFirstSide(side)

                sideRoot2 = parser.FindNode(foodNode, "beilage2")
                sideNodes2 = parser.FindNodes(sideRoot2, "data")
                for sideNode2 in sideNodes2:
                    sideName2 = parser.FindNodeValue(sideNode2, "label")
                    side2 = FoodItem(sideName2)
                    food.AddSecondSide(side2)

                dessertRoot = parser.FindNode(foodNode, "nachspeise")
                dessertNodes = parser.FindNodes(dessertRoot, "data")
                for dessertNode in dessertNodes:
                    dessertName = parser.FindNodeValue(dessertNode, "label")
                    dessert = FoodItem(dessertName)
                    food.AddDessert(dessert)

                menu.AddFood(food)

            mensa.AddMenu(menu)

        self.__Mensas[date] = mensa

    def GetMensa(self, date):
        #return self.__Mensas[date]
        return self.__Mensas[date.strftime(Constants.SWTDateFormat)]

    def HasMensa(self, date):
        return self.__Mensas.has_key(date)