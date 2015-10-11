class Mensa(object):
    """description of class"""

    def __init__(self, id, name, isOpen = True):
        self.Id = id
        self.Name = name
        self.IsOpen = isOpen
        self.Menus = []

    def __str__(self):
        stringRepresentation = self.Name
        if not self.IsOpen:
            stringRepresentation = stringRepresentation + " (geschlossen)"
        return stringRepresentation

    def AddMenu(self, menu):
        self.Menus.append(menu)