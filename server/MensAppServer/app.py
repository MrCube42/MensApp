"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from mensapp.services.parserSWT import ParserSWT
from mensapp.services.transformatorSWT import TransformatorSWT

from mensapp.globals.helpers import Helpers
from mensapp.globals.constants import Constants

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
    startDateString = "20151012"
    endDateString = "20151016"

    startDate = datetime.strptime(startDateString, Constants.SWTDateFormat)
    endDate = datetime.strptime(endDateString, Constants.SWTDateFormat)

    parser = ParserSWT(mensaId, startDateString, endDateString)
    
    mensas = []
    for date in Helpers.GetDatesBetweenIncluding(startDate, endDate):
        mensa = parser.GetMensa(date.strftime(Constants.SWTDateFormat))
        mensas.append(mensa)

    transformator = TransformatorSWT(startDateString, endDateString, mensaId, mensas)

    response = Response(transformator.GetJsonString())
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

    #return parser.GetResult()

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)
