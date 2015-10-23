#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from mensapp.dal.mensaQuery import MensaQuery
from mensapp.dal.mensaTransaction import MensaTransaction

from mensapp.globals.helpers import Helpers
from mensapp.globals.constants import Constants

from mensapp.services.swtParser import SWTParser
from mensapp.services.mensaDecoder import MensaDecoder
from mensapp.services.legacyConverter import LegacyConverter

from mensapp.model.mensa import Mensa

class FoodServer(object):
    """description of class"""

    def __init__(self):
        pass

    def GetJsonOutput(self, mensaId, date):
        mensaEntity = self.__QueryMensaEntity(mensaId, date)
        return mensaEntity.as_json

    def __QueryMensaEntity(self, mensaId, date):
        query = MensaQuery(mensaId, date)
        mensaEntity = None
        if query.HasResult():
            mensaEntity = query.GetResult()
        else:
            mensaEntity = self.__FetchDataFromRemote(mensaId, date)
        return mensaEntity

    def __FetchDataFromRemote(self, mensaId, date):
        # fetch and parse
        parser = SWTParser(mensaId, date)
        if parser.HasMensa(date):
            mensa = parser.GetMensa(date)
            transaction = MensaTransaction(mensa, date)
            transaction.Store()
            mensaEntity = transaction.Get()
        else:
            # no mensa could be fetched -> use placeholder and set not available
            mensa = Mensa(mensaId)
            transaction = MensaTransaction(mensa, date, False)
            transaction.Store()
            mensaEntity = transaction.Get()
        # store and return
        return mensaEntity

    def GetLegacyHtmlJsonOutput(self, mensaId, startDate, endDate):
        mensas = []    
        for date in Helpers.GetDatesBetweenIncluding(startDate, endDate):
            mensaEntity = self.__QueryMensaEntity(mensaId, date)
            # extract the json from the db entity and construct the mensa object from it
            mensa = json.loads(mensaEntity.as_json, cls = MensaDecoder)
            mensas.append(mensa)
        legacyConverter = LegacyConverter(mensaId, startDate, endDate, mensas)
        legacyHtmlJsonString = legacyConverter.GetJsonString()
        return legacyHtmlJsonString