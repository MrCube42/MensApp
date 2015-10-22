#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime

from mensapp.globals.constants import Constants

from mensapp.dal.mensaEntity import MensaEntity
from mensapp.dal.mensaQuery import MensaQuery
from mensapp.dal.mensaTransaction import MensaTransaction

from mensapp.services.swtParser import SWTParser

from mensapp.globals.helpers import Helpers

from mensapp.services.htmlConverter import HtmlConverter

class FoodServer(object):
    """description of class"""

    def __init__(self):
        pass

    def GetJsonOutput(self, mensaId, date):
        query = MensaQuery(mensaId, date)
        mensaEntity = None
        if query.HasResult():
            mensaEntity = query.GetResult()
        else:
            mensaEntity = self.__FetchDataFromRemote(mensaId, date)
        # create json
        return mensaEntity.foods

    def __FetchDataFromRemote(self, mensaId, date):
        # fetch and parse
        parser = SWTParser(mensaId, date)
        mensa = parser.GetMensa(date)
        
        # store and get
        transaction = MensaTransaction(mensa, date)
        transaction.Store()
        mensaEntity = transaction.Get()

        return mensaEntity

    def GetHtmlOutput(self, mensaId, startDate, endDate):
        # for all dates
        mensas = []    
        for date in Helpers.GetDatesBetweenIncluding(startDate, endDate):

            # query
            query = MensaQuery(mensaId, date)
            mensaEntity = None
            if query.HasResult():
                mensaEntity = query.GetResult()
            else:
                # fetch and parse
                parser = SWTParser(mensaId, date)
                mensa = parser.GetMensa(date)
        
                # store and get
                transaction = MensaTransaction(mensa, date)
                transaction.Store()
                mensaEntity = transaction.Get()

                # append
                mensas.append(mensa)

        # create html
        converter = HtmlConverter(startDate, endDate, mensaId, mensas)
        htmlJsonString = converter.GetJsonString()

        return htmlJsonString