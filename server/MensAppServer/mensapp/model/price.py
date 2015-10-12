#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Price(object):
    """description of class"""

    def __init__(self, studentPrice, employeePrice, guestPrice):
        self.__StudentPrice = studentPrice
        self.__EmployeePrice = employeePrice
        self.__GuestPrice = guestPrice

        # TODO: Do we need this?
    #def __str__(self):
    #    return "Student: {0}, Mitarbeiter: {1}, Gast: {2}".format(self.StudentPrice, self.EmployeePrice, self.GuestPrice)

    def GetStudentPrice(self):
        return self.__StudentPrice