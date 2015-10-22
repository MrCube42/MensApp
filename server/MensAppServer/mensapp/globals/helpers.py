#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

class Helpers(object):
    """description of class"""

    @staticmethod
    def GetDatesBetweenIncluding(startDate, endDate):
        dates = []

        currentDate = startDate
        while endDate >= currentDate:
            dates.append(currentDate)
            currentDate = currentDate + timedelta(days = 1)

        return dates