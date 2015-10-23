#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class MensaQuery(object):
    """description of class"""

    def __init__(self, mensaId, date):
        mensaEntities = db.GqlQuery("""
            SELECT *
            FROM MensaEntity
            WHERE mensa_id = :1
            AND date = :2
            """, mensaId, date)
        self.__MensaEntity = mensaEntities.get()

    def HasResult(self):
        return self.__MensaEntity is not None

    def GetResult(self):
        return self.__MensaEntity