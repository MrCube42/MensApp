#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class MensaQuery(object):
    """description of class"""

    def __init__(self, mensaId, date):
        # just return Mensas that are valid and available otherwise they must be updated
        mensaEntities = db.GqlQuery("""
            SELECT *
            FROM MensaEntity
            WHERE mensa_id = :1
            AND date = :2
            AND is_available = True
            """, mensaId, date)
        self.__MensaEntity = mensaEntities.get()

    def HasResult(self):
        return (self.__MensaEntity is not None)

    def GetResult(self):
        return self.__MensaEntity