from mensapp.model.mensa import Mensa
from mensapp.model.menu import Menu
from mensapp.model.food import Food
from mensapp.model.foodItem import FoodItem
from mensapp.model.price import Price

import json

class TransformatorSWT(object):
    """description of class"""

    __OrConnectString = " oder "
    __AndConnectString = ", "

    def __init__(self, startDateString, endDateString, mensaId, mensas, openHours = None):
        self.DateString = "{0}-{1}".format(startDateString, endDateString)
        self.MensaId = mensaId
        self.OpenHours = openHours
        self.Mensas = mensas

    def GetJsonString(self):
        jsonObject = {}
        jsonObject["date"] = self.DateString
        jsonObject["mensaId"] = self.MensaId
        jsonObject["foods"] = self.GetJsonFoods()
        jsonObject["openHours"] = self.OpenHours
        return json.dumps(jsonObject)

    def GetJsonFoods(self):
        foods = []
        for mensa in self.Mensas:
            menus = []
            for menu in mensa.Menus:
                menus.append(self.ConvertMenu(menu))
            foods.append("".join(menus))
        return foods

    def ConvertMenu(self, menu):
        self.Output = ""

        self.AppendToOutput("<div class='theke'>{0}</div>".format(menu.GetName()))

        if menu.IsOpen():
            self.HandleOpenedMenu(menu)
        else:
            self.HandleClosedMenu()
        
        return self.Output

    def HandleOpenedMenu(self, menu):
        self.AppendToOutput("<div class='menu'>")
        for food in menu.GetFoods():
            self.AppendToOutput("<div class='price'>{0}</div>".format(food.GetStudentPrice()))
            self.AppendToOutput("<div class='reference'/>")
            self.HandleMeals(food.GetStarters())
            self.HandleMeals(food.GetMains())
            self.HandleSides(food.GetFirstSides(), food.GetSecondSides())
            self.HandleMeals(food.GetDesserts())
        self.AppendToOutput("</div>")

    def HandleClosedMenu(self):
        self.AppendToOutput("<div class='menu'><div class='price noprice'>-1</div><div class='reference noprice'/><div class='meal'><b>geschlossen</b></div></div>")

    def HandleMeals(self, meals):
        self.AppendToOutput("<div class='meal'>")
        for meal in meals:
            self.AppendToOutput("{0}{1}".format(meal.GetName(), self.__OrConnectString))
        if len(meals) > 0:
            self.RemoveFromOutputEnd(self.__OrConnectString)
        self.AppendToOutput("</div>")

    def HandleSides(self, firstSides, secondSides):
        self.AppendToOutput("<div class='meal'>")

        for side in firstSides:
            self.AppendToOutput("{0}{1}".format(side.GetName(), self.__OrConnectString))
        if len(firstSides) > 0:
            self.RemoveFromOutputEnd(self.__OrConnectString)

        self.AppendToOutput(self.__AndConnectString)

        for side in secondSides:
            self.AppendToOutput("{0}{1}".format(side.GetName(), self.__OrConnectString))
        if len(secondSides) > 0:
            self.RemoveFromOutputEnd(self.__OrConnectString)

        self.AppendToOutput("</div>")

    def AppendToOutput(self, content):
        self.Output = self.Output + content

    def RemoveFromOutputEnd(self, contentToRemove):
        self.Output = self.Output[:-len(contentToRemove)]