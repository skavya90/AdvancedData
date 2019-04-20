# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 18:55:53 2019

@author: skavy
"""
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,and_
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/skavy/Desktop/Bootcamp/AdvancedData/hawaii.sqlite",connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    
    """List all available api routes."""
    return (
        f"Welcome to the Home Page<br/>"
        
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
#####################################################
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    
    last_entry=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_entry = last_entry[0]
    last_year = dt.datetime.strptime(last_entry, '%Y-%m-%d') - dt.timedelta(days=365)
    """Convert the query results to a Dictionary using date as the key and prcp as the value."""
    prcp_result = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        order_by(Measurement.date).all()
    
    p_dict=dict(prcp_result)
    
    """Return the JSON representation of your dictionary."""
    return jsonify(p_dict)

#####################################################
    
@app.route("/api/v1.0/stations")
def stations():
    
    """Return a JSON list of stations from the dataset."""
    stations_result = session.query(Measurement.station).group_by(Measurement.station).all()
    s_list = list(np.ravel(stations_result))
        
    return jsonify(s_list)
#####################################################
        
@app.route("/api/v1.0/tobs")
def tobs():
    
    last_entry=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_entry = last_entry[0]
    last_year = dt.datetime.strptime(last_entry, '%Y-%m-%d') - dt.timedelta(days=365)
    
    """query for the dates and temperature observations from a year from the last data point."""
    tobs_result = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_year).order_by(Measurement.date).all()
    
    t_list=list(np.ravel(tobs_result))
    
    """Return a JSON list of Temperature Observations (tobs) for the previous year.""" 
    return jsonify(t_list)
    
#####################################################
    
@app.route("/api/v1.0/<start>")
def start_date(start):
    
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    strt_date = session.query(func.min(Measurement.tobs), \
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start).all() 
    return jsonify(strt_date)

#####################################################
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    strtend_date = session.query(func.min(Measurement.tobs), \
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(and_(Measurement.date >= start, Measurement.date <= end)).all()
    
    return jsonify(strtend_date)

#####################################################
    
if __name__ == '__main__':
    app.run(debug=False)

