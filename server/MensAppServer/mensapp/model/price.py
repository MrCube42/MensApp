class Price(object):
    """description of class"""

    def __init__(self, studentPrice, employeePrice, guestPrice):
        self.StudentPrice = studentPrice
        self.EmployeePrice = employeePrice
        self.GuestPrice = guestPrice

    def __str__(self):
        return "Student: {0}, Mitarbeiter: {1}, Gast: {2}".format(self.StudentPrice, self.EmployeePrice, self.GuestPrice)

    def GetStudentPrice(self):
        return self.StudentPrice