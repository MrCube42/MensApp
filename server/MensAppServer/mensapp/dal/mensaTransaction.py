#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from mensapp.dal.mensaEntity import MensaEntity
from mensapp.services.jsonConverter import JsonConverter

class MensaTransaction(object):
    """description of class"""

    def __init__(self, mensa, date):
        mensaId = int(mensa.GetId())
        isOpen = mensa.IsOpen()

        # generate json
        menusJson = []
        for menu in mensa.GetMenus():
            menusJson.append(JsonConverter.ConvertMenuToJson(menu))
        jsonString = json.dumps(menusJson)

        # otherwise fetch and store in DB
        self.__MensaEntity = MensaEntity(
            date = date.date(),
            mensa_id = mensaId,
            foods = jsonString,
            is_open = isOpen)

    def Store(self):
        self.__MensaEntity.put()

    def Get(self):
        return self.__MensaEntity