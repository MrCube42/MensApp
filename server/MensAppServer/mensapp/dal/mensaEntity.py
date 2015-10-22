#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from google.appengine.ext import db
from google.appengine.api import users

class MensaEntity(db.Model):
    """description of class"""

    mensa_id = db.IntegerProperty(required=True, indexed=True)
    date = db.DateProperty(required=True)
    is_open = db.BooleanProperty()
    foods = db.TextProperty()