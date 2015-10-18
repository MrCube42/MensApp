#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Price(object):
    """description of class"""

    def __init__(self, studentPrice, employeePrice, guestPrice):
        self.__StudentPrice = studentPrice
        self.__EmployeePrice = employeePrice
        self.__GuestPrice = guestPrice

    def GetStudentPrice(self):
        return self.__StudentPrice

    def GetEmployeePrice(self):
        return self.__EmployeePrice

    def GetGuestPrice(self):
        return self.__GuestPrice