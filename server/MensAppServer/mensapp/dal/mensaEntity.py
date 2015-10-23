#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class MensaEntity(db.Model):
    """description of class"""

    mensa_id = db.IntegerProperty(required=True, indexed=True)
    date = db.DateProperty(required=True)
    is_open = db.BooleanProperty(required=True)
    as_json = db.TextProperty(required=True)