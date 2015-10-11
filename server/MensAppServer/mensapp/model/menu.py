class Menu(object):
    """description of class"""

    def __init__(self, name, isOpen = True):
        self.__Name = name
        self.__IsOpen = isOpen
        self.__Foods = []

    def __str__(self):
        stringRepresentation = self.__Name
        if not self.IsOpen():
            stringRepresentation = stringRepresentation + " (geschlossen)"
        return stringRepresentation

    def AddFood(self, food):
        self.__Foods.append(food)

    def GetName(self):
        return self.__Name

    def GetFoods(self):
        return self.__Foods

    def IsOpen(self):
        return self.__IsOpen