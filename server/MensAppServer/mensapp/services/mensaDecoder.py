#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import JSONDecoder

from mensapp.globals.constants import Constants

from mensapp.model.mensa import Mensa
from mensapp.model.menu import Menu
from mensapp.model.food import Food
from mensapp.model.price import Price
from mensapp.model.foodItem import FoodItem

class MensaDecoder(JSONDecoder):
    """description of class"""

    def __init__(self, *args, **kargs):
       JSONDecoder.__init__(self, object_hook=self.__ConvertJsonToObject, *args, **kargs)

    def __ConvertJsonToObject(self, jsonObject):
        object = None
        if jsonObject.has_key(Constants.JSON_TYPE_KEY):
            typename = jsonObject.pop(Constants.JSON_TYPE_KEY)
            if typename == FoodItem.__name__:
                object = self.__ConvertJsonToFoodItem(jsonObject)
            elif typename == Price.__name__:
                object = self.__ConvertJsonToPrice(jsonObject)
            elif typename == Food.__name__:
                object = self.__ConvertJsonToFood(jsonObject)
            elif typename == Menu.__name__:
                object = self.__ConvertJsonToMenu(jsonObject)
            elif typename == Mensa.__name__:
                object = self.__ConvertJsonToMensa(jsonObject)
        return object

    def __ConvertJsonToMensa(self, jsonObject):
        id = jsonObject[Constants.JSON_ID_KEY]
        name = jsonObject[Constants.JSON_NAME_KEY]
        isOpen = jsonObject[Constants.JSON_IS_OPEN_KEY]
        mensa = Mensa(id, name, isOpen)
        for menu in jsonObject[Constants.JSON_MENUS_KEY]:
            mensa.AddMenu(menu)
        return mensa

    def __ConvertJsonToMenu(self, jsonObject):
        name = jsonObject[Constants.JSON_NAME_KEY]
        isOpen = jsonObject[Constants.JSON_IS_OPEN_KEY]
        menu = Menu(name, isOpen)
        for food in jsonObject[Constants.JSON_FOODS_KEY]:
            menu.AddFood(food)
        return menu

    def __ConvertJsonToFood(self, jsonObject):
        name = jsonObject[Constants.JSON_NAME_KEY]
        description = jsonObject[Constants.JSON_DESCRIPTION_KEY]
        price = jsonObject[Constants.JSON_PRICE_KEY]
        food = Food(name, description, price)
        for starter in jsonObject[Constants.JSON_STARTERS_KEY]:
            food.AddStarter(starter)
        for main in jsonObject[Constants.JSON_MAINS_KEY]:
            food.AddMain(main)
        for firstSide in jsonObject[Constants.JSON_FIRST_SIDES_KEY]:
            food.AddFirstSide(firstSide)
        for secondSide in jsonObject[Constants.JSON_SECOND_SIDES_KEY]:
            food.AddSecondSide(secondSide)
        for dessert in jsonObject[Constants.JSON_DESSERTS_KEY]:
            food.AddDessert(dessert)
        return food

    def __ConvertJsonToPrice(self, jsonObject):
        studentPrice = jsonObject[Constants.JSON_STUDENT_PRICE_KEY]
        employeePrice = jsonObject[Constants.JSON_EMPLOYEE_PRICE_KEY]
        guestPrice = jsonObject[Constants.JSON_GUEST_PRICE_KEY]
        return Price(studentPrice, employeePrice, guestPrice)

    def __ConvertJsonToFoodItem(self, jsonObject):
        name = jsonObject[Constants.JSON_NAME_KEY]
        return FoodItem(name)