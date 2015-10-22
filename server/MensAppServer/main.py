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

        #parser = ParserSWT(mensaId, startDateString, endDateString)
        
        #dateString = startDate.strftime(Constants.SWTDateFormat)
        #if parser.HasMensa(dateString):
        #    mensa = parser.GetMensa(dateString)
        #    #mensas.append(mensa)

        #    # generate json
        #    menusJson = []
        #    for menu in mensa.GetMenus():
        #        menusJson.append(JsonConverter.ConvertMenuToJson(menu))

        #    jsonString = json.dumps(menusJson)
            
        #    query = MensaQuery(mensaId, startDate)
        #    mensaEntity = query.GetResult()
        #    if mensaEntity is not None:
        #        logging.info(mensaEntity)
        #    else:
        #        transaction = MensaTransaction(mensa, startDate)
        #        transaction.Store()
                ## otherwise fetch and store in DB
                #mensaEntity = MensaEntity(
                #    date = startDate.date(),
                #    mensa_id = int(mensaId),
                #    foods = jsonString,
                #    is_open = mensa.IsOpen())
                #mensaEntity.put()

        #for date in Helpers.GetDatesBetweenIncluding(startDate, endDate):
        #    dateString = date.strftime(Constants.SWTDateFormat)
        #    if parser.HasMensa(dateString):
        #        mensa = parser.GetMensa(dateString)
    
            ## generate json
            #menusJson = []
            #for menu in mensa.GetMenus():
            #    menusJson.append(JsonConverter.ConvertMenuToJson(menu))
            #jsonObject[mensaId + date.strftime(Constants.SWTDateFormat)] = menusJson

            ## revert json
            #for menjuJson in menusJson:
            #    menu = JsonConverter.ConvertJsonToMenu(menjuJson)
            #    print menu.GetName()
            #    for food in menu.GetFoods():
            #        print food.GetName()
            #        print food.GetPrice().GetStudentPrice()
            #        for main in food.GetMains():
            #            print main.GetName()

        #transformator = TransformatorSWT(startDateString, endDateString, mensaId, mensas)

        #jsonString = transformator.GetJsonString()
        #jsonString = json.dumps(jsonObject, ensure_ascii = False, indent = 2, sort_keys = True)
        #self.response.headers['Access-Control-Allow-Origin'] = '*'
        ##self.response.write(jsonString)
        #self.response.write("done")

        # TODO: Handle parsed data (write to file, in DB or elsewhere)
        #filename = u"{0}_mensafood_{1}-{2}_2.0.xml".format(mensaId, startDateString, endDateString)
        #with open(filename, 'w') as outfile:
        #    outfile.write(json)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)