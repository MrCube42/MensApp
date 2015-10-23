#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import JSONEncoder

from mensapp.globals.constants import Constants

from mensapp.model.mensa import Mensa
from mensapp.model.menu import Menu
from mensapp.model.food import Food
from mensapp.model.price import Price
from mensapp.model.foodItem import FoodItem

class MensaEncoder(JSONEncoder):
    """description of class"""

    def default(self, obj):
        if isinstance(obj, Price):
            return self.__ConvertPriceToJson(obj)
        elif isinstance(obj, FoodItem):
            return self.__ConvertFoodItemToJson(obj)
        elif isinstance(obj, Food):
            return self.__ConvertFoodToJson(obj)
        elif isinstance(obj, Menu):
            return self.__ConvertMenuToJson(obj)
        elif isinstance(obj, Mensa):
            return self.__ConvertMensaToJson(obj)
        return JSONEncoder.default(self, obj)

    def __ConvertMensaToJson(self, mensa):
        jsonObject = {}
        jsonObject[Constants.JSON_TYPE_KEY] = type(mensa).__name__
        jsonObject[Constants.JSON_ID_KEY] = mensa.GetId()
        jsonObject[Constants.JSON_NAME_KEY] = mensa.GetName()
        jsonObject[Constants.JSON_IS_OPEN_KEY] = mensa.IsOpen()
        menus = mensa.GetMenus()
        jsonObject[Constants.JSON_MENUS_KEY] = self.__CreateJsonListFromMenuList(menus)
        return jsonObject

    def __ConvertMenuToJson(self, menu):
        jsonObject = {}
        jsonObject[Constants.JSON_TYPE_KEY] = type(menu).__name__
        jsonObject[Constants.JSON_NAME_KEY] = menu.GetName()
        jsonObject[Constants.JSON_IS_OPEN_KEY] = menu.IsOpen()
        foods = menu.GetFoods()
        jsonObject[Constants.JSON_FOODS_KEY] = self.__CreateJsonListFromFoodList(foods)
        return jsonObject

    def __ConvertFoodToJson(self, food):
        jsonObject = {}
        jsonObject[Constants.JSON_TYPE_KEY] = type(food).__name__
        jsonObject[Constants.JSON_NAME_KEY] = food.GetName()
        jsonObject[Constants.JSON_DESCRIPTION_KEY] = food.GetDescription()
        price = food.GetPrice()
        jsonObject[Constants.JSON_PRICE_KEY] = self.__ConvertPriceToJson(price)
        starters = food.GetStarters()
        jsonObject[Constants.JSON_STARTERS_KEY] = self.__CreateJsonListFromFoodItemList(starters)
        mains = food.GetMains()
        jsonObject[Constants.JSON_MAINS_KEY] = self.__CreateJsonListFromFoodItemList(mains)
        firstSides = food.GetFirstSides()
        jsonObject[Constants.JSON_FIRST_SIDES_KEY] = self.__CreateJsonListFromFoodItemList(firstSides)
        secondSides = food.GetSecondSides()
        jsonObject[Constants.JSON_SECOND_SIDES_KEY] = self.__CreateJsonListFromFoodItemList(secondSides)
        desserts = food.GetDesserts()
        jsonObject[Constants.JSON_DESSERTS_KEY] = self.__CreateJsonListFromFoodItemList(desserts)
        return jsonObject

    def __ConvertPriceToJson(self, price):
        jsonObject = {}
        jsonObject[Constants.JSON_TYPE_KEY] = type(price).__name__
        jsonObject[Constants.JSON_STUDENT_PRICE_KEY] = price.GetStudentPrice()
        jsonObject[Constants.JSON_EMPLOYEE_PRICE_KEY] = price.GetEmployeePrice()
        jsonObject[Constants.JSON_GUEST_PRICE_KEY] = price.GetGuestPrice()
        return jsonObject

    def __ConvertFoodItemToJson(self, foodItem):
        jsonObject = {}
        jsonObject[Constants.JSON_TYPE_KEY] = type(foodItem).__name__
        jsonObject[Constants.JSON_NAME_KEY] = foodItem.GetName()
        return jsonObject

    ### Helpers ###
    def __CreateJsonListFromFoodItemList(self, foodItems):
        foodItemsJson = []
        for foodItem in foodItems:
            foodItemJson = self.__ConvertFoodItemToJson(foodItem)
            foodItemsJson.append(foodItemJson)
        return foodItemsJson
 
    def __CreateJsonListFromFoodList(self, foods):
        foodsJson = []
        for food in foods:
            foodJson = self.__ConvertFoodToJson(food)
            foodsJson.append(foodJson)
        return foodsJson

    def __CreateJsonListFromMenuList(self, menus):
        menusJson = []
        for menu in menus:
            menuJson = self.__ConvertMenuToJson(menu)
            menusJson.append(menuJson)
        return menusJson