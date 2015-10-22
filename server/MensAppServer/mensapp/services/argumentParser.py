from datetime import datetime

from mensapp.globals.constants import Constants

import logging

class ArgumentParser(object):
    """description of class"""

    __MENSA_ID_ARGUMENT_KEY = "mensa"
    __DATE_ARGUMENT_KEY = "date"
    __DATESPAN_ARGUMENT_KEY = "datespan"

    __MensaId = None
    __Date = None
    __StartDate = None
    __EndDate = None

    def __init__(self, request):
        mensaIdString = request.get(self.__MENSA_ID_ARGUMENT_KEY)
        dateString = request.get(self.__DATE_ARGUMENT_KEY)
        dateSpanString = request.get(self.__DATESPAN_ARGUMENT_KEY)
        if mensaIdString is not None and len(mensaIdString) > 0:
            self.__MensaId = int(mensaIdString)
        if dateString is not None and len(dateString) > 0:
            self.__Date = datetime.strptime(dateString, Constants.SWTDateFormat)
        if dateSpanString is not None and len(dateSpanString) > 0:
            self.__ParseDateSpan(dateSpanString)

    def __ParseDateSpan(self, dateSpanString):
        dates = dateSpanString.split("-")
        if len(dates) == 2:
            self.__StartDate = datetime.strptime(dates[0], Constants.SWTDateFormat)
            self.__EndDate = datetime.strptime(dates[1], Constants.SWTDateFormat)

    def HasMensaId(self):
        return self.__MensaId is not None

    def GetMensaId(self):
        return self.__MensaId

    def HasDate(self):
        return self.__Date is not None

    def GetDate(self):
        return self.__Date

    def HasDateSpan(self):
        hasStartDate = self.__StartDate is not None
        hasEndDate = self.__EndDate is not None
        return hasStartDate and hasEndDate

    def GetStartDate(self):
        return self.__StartDate

    def GetEndDate(self):
        return self.__EndDate