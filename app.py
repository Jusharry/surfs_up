import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Access the SQLite database
engine = create_engine('sqlite:///hawaii.sqlite')
#Reflect the database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session=Session(engine)
#Setup flask
app = Flask(__name__)
@app.route('/')
def welcome():
    return(
            '''  
        Welcome to the Climate Analysis API!<br/>
        Available Routes:<br/>
        <a href="http://127.0.0.1:5000/api/v1.0/precipitation" target="_blank">Precipitation</a><br/>
        <a href="http://127.0.0.1:5000/api/v1.0/stations" target="_blank_">Stations</a><br/>
        <a href="http://127.0.0.1:5000/api/v1.0/tobs" target="_blank_">Temps</a><br/>
        <a href="http://127.0.0.1:5000/api/v1.0/temp/start/end" target="_blank_">Start/End</a>

    '''
        )

@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():
    results= session.query(Station.station).all()
    #converts results to a list after taking making a 1 dimensional array from query results
    stations = list(np.ravel(results))
    #see https://flask.palletsprojects.com/en/2.0.x/api/#flask.json.jsonify keyword args.
    return jsonify(stations=stations)

@app.route('/api/v1.0/tobs')
def temp_monthly():
     prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
     results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
     temps= list(np.ravel(results))
     return jsonify(temps=temps)

@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start=None, end=None):
    sel=[func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if not end:
        #(*sel) indicates that query will return multiple results
        results = session.query(*sel).filter(Measurement.date >= start).all()
        temps=list(np.ravel(results))
    # start=dt.date(input("Enter start date: "))
    # end=dt.date(input("Enter end date: "))
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps= list(np.ravel(results))
    return jsonify(temps)