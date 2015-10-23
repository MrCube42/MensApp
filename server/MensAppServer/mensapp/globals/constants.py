#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Constants(object):
    """description of class"""

    SWTDateFormat = "%Y%m%d"

    ### JSON Keys ###
    ## General ##
    JSON_TYPE_KEY = "__type__"
    JSON_NAME_KEY = "Name"

    ## Price ##
    JSON_STUDENT_PRICE_KEY = "StudentPrice"
    JSON_EMPLOYEE_PRICE_KEY = "EmployeePrice"
    JSON_GUEST_PRICE_KEY = "GuestPrice"

    ## Food ##
    JSON_DESCRIPTION_KEY = "Description"
    JSON_PRICE_KEY = "Price"
    JSON_STARTERS_KEY = "Starters"
    JSON_MAINS_KEY = "Mains"
    JSON_FIRST_SIDES_KEY = "FirstSides"
    JSON_SECOND_SIDES_KEY = "SecondSides"
    JSON_DESSERTS_KEY = "Desserts"

    ## Menu ##
    JSON_IS_OPEN_KEY = "IsOpen"
    JSON_FOODS_KEY = "Foods"

    ## Mensa ##
    JSON_ID_KEY = "Id"
    JSON_MENUS_KEY = "Menus"