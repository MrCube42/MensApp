#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

# Overwrite default encoding!
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding("utf-8")

from mensapp.services.parserSWT import ParserSWT
from mensapp.services.transformatorSWT import TransformatorSWT

from mensapp.globals.helpers import Helpers
from mensapp.globals.constants import Constants

import json

from mensapp.services.jsonConverter import JsonConverter

from datetime import date
from datetime import datetime

from flask import Flask
from flask import request
from flask import Response
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def getFood():
    """Renders a sample page."""

    mensaId = request.args.get('mensa')
    startDateString = "20151019"
    endDateString = "20151023"

    startDate = datetime.strptime(startDateString, Constants.SWTDateFormat)
    endDate = datetime.strptime(endDateString, Constants.SWTDateFormat)

    parser = ParserSWT(mensaId, startDateString, endDateString)

    jsonObject = {}
    mensas = []
    for date in Helpers.GetDatesBetweenIncluding(startDate, endDate):
        mensa = parser.GetMensa(date.strftime(Constants.SWTDateFormat))
        mensas.append(mensa)
    
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

    transformator = TransformatorSWT(startDateString, endDateString, mensaId, mensas)

    jsonString = transformator.GetJsonString()
    #jsonString = json.dumps(jsonObject, ensure_ascii = False, indent = 2, sort_keys = True)
    response = Response(jsonString)
    response.headers['Access-Control-Allow-Origin'] = '*'

    # TODO: Handle parsed data (write to file, in DB or elsewhere)
    #filename = u"{0}_mensafood_{1}-{2}_2.0.xml".format(mensaId, startDateString, endDateString)
    #with open(filename, 'w') as outfile:
    #    outfile.write(json)

    return response

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)