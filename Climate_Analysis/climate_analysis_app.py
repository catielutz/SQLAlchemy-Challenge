import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def Homepage():
    """List all routes that are available."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).all()
    rain_dict = {}
    for date, prcp in prcp_data:
        rain_dict[date] = prcp
    return jsonify(rain_dict)
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    try:
        stations = session.query(Station.station, Station.name).all()
        stations_list = list(np.ravel(stations))
        return jsonify(stations_list)
    except:
        print("Error!")
    finally:
        session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    try:
        query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        waihee_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= query_date).all()
        tobs = list(np.ravel(waihee_year))
        return jsonify(tobs)
    except:
        print("Error!")
    finally:
        session.close()

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temps(start=None, end=None):
    session = Session(engine)
    if not end:
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        temp_list = list(np.ravel(temps))
        return jsonify(temp_list)
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_list = list(np.ravel(temps))
    return jsonify(temp_list)
    session.close()

    

if __name__ == '__main__':
    app.run(debug=True)