#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mensapp.model.mensa import Mensa
from mensapp.model.menu import Menu
from mensapp.model.food import Food
from mensapp.model.foodItem import FoodItem
from mensapp.model.price import Price

import json

class JsonConverter(object):
    """description of class"""

    ### Keys ###
    __NAME_KEY = "Name"

    ### Price ###
    __STUDENT_PRICE_KEY = "StudentPrice"
    __EMPLOYEE_PRICE_KEY = "EmployeePrice"
    __GUEST_PRICE_KEY = "GuestPrice"

    @staticmethod
    def ConvertPriceToJson(price):
        jsonObject = {}
        jsonObject[JsonConverter.__STUDENT_PRICE_KEY] = price.GetStudentPrice()
        jsonObject[JsonConverter.__EMPLOYEE_PRICE_KEY] = price.GetEmployeePrice()
        jsonObject[JsonConverter.__GUEST_PRICE_KEY] = price.GetGuestPrice()
        return jsonObject

    @staticmethod
    def ConvertJsonToPrice(jsonObject):
        # TODO: Ensure that keys are available and object correct
        studentPrice = jsonObject[JsonConverter.__STUDENT_PRICE_KEY]
        employeePrice = jsonObject[JsonConverter.__EMPLOYEE_PRICE_KEY]
        guestPrice = jsonObject[JsonConverter.__GUEST_PRICE_KEY]
        price = Price(studentPrice, employeePrice, guestPrice)
        return price

    ### FoodItem ###
    @staticmethod
    def ConvertFoodItemToJson(foodItem):
        jsonObject = {}
        jsonObject[JsonConverter.__NAME_KEY] = foodItem.GetName()
        return jsonObject

    @staticmethod
    def ConvertJsonToFoodItem(jsonObject):
        # TODO: Ensure that keys are available and object correct
        name = jsonObject[JsonConverter.__NAME_KEY]
        foodItem = FoodItem(name)
        return foodItem

    ### Food ###
    __DESCRIPTION_KEY = "Description"
    __PRICE_KEY = "Price"
    __STARTERS_KEY = "Starters"
    __MAINS_KEY = "Mains"
    __FIRST_SIDES_KEY = "FirstSides"
    __SECOND_SIDES_KEY = "SecondSides"
    __DESSERTS_KEY = "Desserts"
    
    @staticmethod
    def __CreateJsonListFromFoodList(foodList):
        jsonList = []
        for foodItem in foodList:
            foodItemJson = JsonConverter.ConvertFoodItemToJson(foodItem)
            jsonList.append(foodItemJson)
        return jsonList
        
    @staticmethod
    def ConvertFoodToJson(food):
        jsonObject = {}
        jsonObject[JsonConverter.__NAME_KEY] = food.GetName()
        jsonObject[JsonConverter.__DESCRIPTION_KEY] = food.GetDescription()
        
        price = food.GetPrice()
        jsonObject[JsonConverter.__PRICE_KEY] = JsonConverter.ConvertPriceToJson(price)

        starters = food.GetStarters()
        jsonObject[JsonConverter.__STARTERS_KEY] = JsonConverter.__CreateJsonListFromFoodList(starters)
        mains = food.GetMains()
        jsonObject[JsonConverter.__MAINS_KEY] = JsonConverter.__CreateJsonListFromFoodList(mains)
        firstSides = food.GetFirstSides()
        jsonObject[JsonConverter.__FIRST_SIDES_KEY] = JsonConverter.__CreateJsonListFromFoodList(firstSides)
        secondSides = food.GetMains()
        jsonObject[JsonConverter.__SECOND_SIDES_KEY] = JsonConverter.__CreateJsonListFromFoodList(secondSides)
        desserts = food.GetDesserts()
        jsonObject[JsonConverter.__DESSERTS_KEY] = JsonConverter.__CreateJsonListFromFoodList(desserts)

        return jsonObject

    @staticmethod
    def ConvertJsonToFood(jsonObject):
        # TODO: Ensure that keys are available and object correct
        name = jsonObject[JsonConverter.__NAME_KEY]
        description = jsonObject[JsonConverter.__DESCRIPTION_KEY]
        
        priceJson = jsonObject[JsonConverter.__PRICE_KEY]
        price = JsonConverter.ConvertJsonToPrice(priceJson)
        
        food = Food(name, description, price)

        startersJsonList = jsonObject[JsonConverter.__STARTERS_KEY]
        for starterJson in startersJsonList:
            starter = JsonConverter.ConvertJsonToFoodItem(starterJson)
            food.AddStarter(starter)
        mainsJsonList = jsonObject[JsonConverter.__MAINS_KEY]
        for mainJson in mainsJsonList:
            main = JsonConverter.ConvertJsonToFoodItem(mainJson)
            food.AddMain(main)
        firstSidesJsonList = jsonObject[JsonConverter.__FIRST_SIDES_KEY]
        for firstSideJson in firstSidesJsonList:
            firstSide = JsonConverter.ConvertJsonToFoodItem(firstSideJson)
            food.AddFirstSide(firstSide)
        secondSidesJsonList = jsonObject[JsonConverter.__SECOND_SIDES_KEY]
        for secondSideJson in secondSidesJsonList:
            secondSide = JsonConverter.ConvertJsonToFoodItem(secondSideJson)
            food.AddSecondSide(secondSide)
        dessertsJsonList = jsonObject[JsonConverter.__DESSERTS_KEY]
        for dessertJson in dessertsJsonList:
            dessert = JsonConverter.ConvertJsonToFoodItem(dessertJson)
            food.AddDessert(dessert)

        return food

    ### Menu ###
    __IS_OPEN_KEY = "IsOpen"
    __FOODS_KEY = "Foods"

    @staticmethod
    def ConvertMenuToJson(menu):
        jsonObject = {}
        jsonObject[JsonConverter.__NAME_KEY] = menu.GetName()
        jsonObject[JsonConverter.__IS_OPEN_KEY] = menu.IsOpen()

        foodsJson = []
        for food in menu.GetFoods():
            foodJson = JsonConverter.ConvertFoodToJson(food)
            foodsJson.append(foodJson)

        jsonObject[JsonConverter.__FOODS_KEY] = foodsJson

        return jsonObject

    @staticmethod
    def ConvertJsonToMenu(jsonObject):
        name = jsonObject[JsonConverter.__NAME_KEY]
        isOpen = jsonObject[JsonConverter.__IS_OPEN_KEY]

        menu = Menu(name, isOpen)

        foodsJsonList = jsonObject[JsonConverter.__FOODS_KEY]
        for foodJson in foodsJsonList:
            food = JsonConverter.ConvertJsonToFood(foodJson)
            menu.AddFood(food)

        return menu