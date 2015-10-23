#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from mensapp.dal.mensaEntity import MensaEntity

from mensapp.services.mensaEncoder import MensaEncoder

class MensaTransaction(object):
    """description of class"""

    def __init__(self, mensa, date):
        mensaId = int(mensa.GetId())
        isOpen = mensa.IsOpen()
        asJson = json.dumps(mensa, cls = MensaEncoder, ensure_ascii = False, sort_keys = True, indent = 1)
        self.__MensaEntity = MensaEntity(
            date = date.date(),
            mensa_id = mensaId,
            as_json = asJson,
            is_open = isOpen)

    def Store(self):
        self.__MensaEntity.put()

    def Get(self):
        return self.__MensaEntity