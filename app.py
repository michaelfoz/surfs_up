# CODE COMMENTED OUT (from Module 9.4.3 Set Up Flask and Create a Route)
# https://courses.bootcampspot.com/courses/1225/pages/9-dot-4-3-set-up-flask-and-create-a-route?module_item_id=498378
# Import Flask Dependency
# from flask import Flask

# Create a New Flask App Instance
# app = Flask(__name__)

# Create Flask Routes
# @app.route('/')
# def hello_world(): # create a function called hello_world()
#    return 'Hello world'
# ---END OF MODULE 9.4.3---
# (Commented out because Module 9.5.1 has instructions to create new file with the same name "app.py")



# Module 9.5.1 Set Up the Database and Flask (below)
# https://courses.bootcampspot.com/courses/1225/pages/9-dot-5-1-set-up-the-database-and-flask?module_item_id=498387

# Set Up the Flask Weather App
# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import dependencies for SQLAlchemny
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import dependency for Flask
from flask import Flask, jsonify

# ---Set Up the Database---
engine = create_engine("sqlite:///hawaii.sqlite") 
# create_engine--allows access the SQLite database and query the SQLite database file

# Reflect the database intot the classes
Base = automap_base()
Base.prepare(engine, reflect=True)
# Base.prepare()--is a Python Flask function used to reflect the tables

# Save the references to each table/create variables for each class
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)
# ---Set Up the Database finished---



# ---Set Up Flask---

# Define the Flask app
app = Flask(__name__)

# About "__name__"
# __name__ is a special type of variable in Python. 
# Its value depends on where and how the code is run.
# e.g., if we wanted to import our app.py file into another Python file named example.py, 
# the variable __name__ would be set to example.
# However, when we run the script with python app.py, the __name__ variable will be set to __main__. 
# This indicates that we are not using any other file to run this code.

# Module 9.5.2 Create the Welcome Route
# https://courses.bootcampspot.com/courses/1225/pages/9-dot-5-2-create-the-welcome-route?module_item_id=498393

# BEFORE STARTING--IMPORTANT
# All of your routes should go after the app = Flask(__name__) line of code. Otherwise, your code may not run properly.

# Define the welcome route
@app.route("/")

# Add the routing information for each of the other routes: 
# 1. Create a function welcome() with a return statement
# 2. Add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement. 
# Use f-strings to display them for our investors:

# (When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route. 
# This convention signifies that this is version 1 of our application. 
# This line can be updated to support future versions of the app as well.)

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')



# Module 9.5.3 Precipitation Route
# The next route we'll build is for the precipitation analysis. 
# This route will occur separately from the welcome route.
# CAUTION
# Every time you create a new route, your code should be aligned to the left in order to avoid errors.

# Create the Route
@app.route("/api/v1.0/precipitation")

# Create the precipitation() function
def precipitation():
   # Calculate the date one year ago from the most recent date in the database
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
   # Query--get the date and precipitation for the previous year
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   # Create a dictionary with the date as the key and the precipitation as the value
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
   #  Jsonify()--a function that converts the dictionary to a JSON file

# .\ is used to signify query to continue on the next line. 
#  You can use the combination of .\ to shorten the length of your query line so that it extends to the next line.



# Module 9.5.4 Stations Route
# https://courses.bootcampspot.com/courses/1225/pages/9-dot-5-4-stations-route?module_item_id=498403

@app.route("/api/v1.0/stations")

def stations():
    # Query--get all of the stations in the database
    results = session.query(Station.station).all()
    # Unravel results into a one-dimensional array
    stations = list(np.ravel(results))
    # Convert unraveled results into a list
    return jsonify(stations=stations)
    # To return our list as JSON, we need to add stations=stations. This formats our list into JSON.



# Module 9.5.5 Monthly Temperature Route
# https://courses.bootcampspot.com/courses/1225/pages/9-dot-5-5-monthly-temperature-route?module_item_id=498409
# For this route, the goal is to return the temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Calculate the date one year ago from the last date in the database
    # (This is the same date as the one we calculated previously.)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    # Unravel the results into a one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    # Jsonify the list and return the results
    return jsonify(temps=temps)



# Module 9.5.6 Statistics Route
# https://courses.bootcampspot.com/courses/1225/pages/9-dot-5-6-statistics-route?module_item_id=498416
# This last route will be to report on the minimum, average, and maximum temperatures. 
# This route is different from the previous ones in that we will have to provide both a starting and ending date.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    # Query to select the minimum, average, and maximum temperatures from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # if-not statement helps determine the starting and ending date
    if not end:
        # Asterisk--indicates there will be multiple results for our query: minimum, average, and maximum temperatures.
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)