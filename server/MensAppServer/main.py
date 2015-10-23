#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

# Overwrite default encoding!
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding("utf-8")

import webapp2

from mensapp.services.argumentParser import ArgumentParser
from mensapp.services.foodServer import FoodServer

class MainHandler(webapp2.RequestHandler):
    def get(self):
        """TODO: Description..."""

        argumentParser = ArgumentParser(self.request)
        if not argumentParser.HasMensaId():
            # Error: Should never happen
            response.write("You must provide a Mensa-ID as argument '?mensa='.")
        mensaId = argumentParser.GetMensaId()

        if argumentParser.HasDateSpan():
            # Query span
            startDate = argumentParser.GetStartDate()
            endDate = argumentParser.GetEndDate()
            foodServer = FoodServer()
            htmlString = foodServer.GetHtmlOutput(mensaId, startDate, endDate)
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.write(htmlString)
        
        elif argumentParser.HasDate():
            # Query single date
            date = argumentParser.GetDate()
            foodServer = FoodServer()
            jsonString = foodServer.GetJsonOutput(mensaId, date)
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.write(jsonString)

        # TODO: Handle parsed data (write to file, in DB or elsewhere)
        #filename = u"{0}_mensafood_{1}-{2}_2.0.xml".format(mensaId, startDateString, endDateString)
        #with open(filename, 'w') as outfile:
        #    outfile.write(json)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)