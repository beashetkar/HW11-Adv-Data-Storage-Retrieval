##############################################################################
#  Step 4 - Climate App
# ###########################################################################  

# Import Dependencies

#import pandas as pd
import numpy as np
from datetime import datetime, date

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
print("Connected to DB hawaii.sqllite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print("Reflected tables")

# Assign the measurement and station  classes to the variables called `Measurements` and 'Stations'
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Create the session from Python to the DB
session = Session(engine)

##########################################################################
# Function for calculating days
##########################################################################

def get_start_date(end_date,t_move):

    endDate = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # vacation trip was 12 days long
    trip = 12

    # reconstruct date fully
    if t_move == 'Y' :
        startDate = datetime(endDate.year - 1, endDate.month, endDate.day)
    else:
        startDate = datetime(endDate.year, endDate.month, endDate.day-trip)
      
    datetime.strftime(startDate, "%Y-%m-%d").replace(' 0', ' ')
    return (datetime.strftime(startDate, "%Y-%m-%d").replace(' 0', ' '))

# Get the last date of the data and find the date one year ago.
qry = session.query(func.max(Measurements.date).label("last_date"))
res = qry.one()
last_date = res.last_date
year_ago_date = get_start_date(last_date, 'Y')

# Find the matching days from the previous years.
end_date = year_ago_date
start_date = get_start_date(end_date, 'N')

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""

    return (
        f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation - List of Precipitation<br/>"

        f"/api/v1.0/stations"
        f"- List of Stations<br/>"

        f"/api/v1.0/tobs"
        f"- List of Temperatures Observations of Previous Year<br/>"

        f"/api/v1.0/<start_date>"
        f"- List of the Min,  the Max and the Avg temperature  for all dates greater greater than or equal to the start date<br/>"

        f"/api/v1.0/<start_date>/<end_date>"
        f"- List of the Min,  the Max and the Avg temperature  for all dates between the start date and end date<br/>"
    )
   
# Route /api/v1.0/precipitation
# Query for the dates and precipitation observations from the last year.
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the json representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    last_12_prcp = session.query(Measurements.date,Measurements.prcp).\
                                 filter(Measurements.date.between(year_ago_date, last_date)).\
                                 order_by(Measurements.date.asc()).all()
            
    prcp_data = []
    for rec_prcp in last_12_prcp:
        prcp_dict = {}
        prcp_dict["date"] = rec_prcp.date
        prcp_dict["prcp"] = rec_prcp.prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

# Route /api/v1.0/stations
# Return a json list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    
    list_of_stations = session.query(Stations.station, Stations.name).all()
    
    stations_data = []
    for rec_station in list_of_stations:
        station_dict = {}
        station_dict["sation"] = rec_station.station
        station_dict["name"] = rec_station.name
        stations_data.append(station_dict)
        
    return jsonify(stations_data)

# Route /api/v1.0/tobs
# Return a json list of Temperature Observations (tobs) for the previous year

@app.route("/api/v1.0/tobs")
def tobs():
    
    last_12_tobs = session.query(Measurements.date, Measurements.tobs).\
                                 filter(Measurements.date.between(start_date, end_date)).\
                                 order_by(Measurements.date).all()

    tobs_data = []
    for rec_tobs in last_12_tobs:
        tobs_dict = {}
        tobs_dict["date"] = rec_tobs.date
        tobs_dict["tobs"] = rec_tobs.tobs
        tobs_data.append(tobs_dict)
    
    return jsonify(tobs_data)    

# Route /api/v1.0/<start>
# Return a json list of the minimum temperature, the average temperature, and the max temperature  
# for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start_date>")
def temp_range_start(start_date):
    
    res_temps = session.query(func.min(Measurements.tobs).label("temp_min"),\
                             func.avg(Measurements.tobs).label("temp_avg"),\
                             func.max(Measurements.tobs).label("temp_max")).\
                             filter(Measurements.date >= start_date).first()

    temps_data = list(np.ravel(res_temps))            
    return jsonify(temps_data)

# Route /api/v1.0/<start>
# Return a json list of the minimum temperature, the average temperature, and the max temperature  
# for all dates between the start date and end date.

@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_start_end(start_date,end_date):
    
    res_temps = session.query(func.min(Measurements.tobs).label("temp_min"),\
                             func.avg(Measurements.tobs).label("temp_avg"),\
                             func.max(Measurements.tobs).label("temp_max")).\
                             filter(Measurements.date.between(start_date, end_date)).first()
        
    temps_data = list(np.ravel(res_temps))
    return jsonify(temps_data)

if __name__ == "__main__":
    app.run(debug=False)   

