# Impoert various modules
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from flask import Flask, jsonify
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the json list of tobs for the last 12 months"""
    precip_last_12_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= '2017-01-15', Measurement.date >= '2016-01-16').all()


    tobs_data = []
    for rec in range(len(precip_last_12_months)):
        tobs_dict = {}
        tobs_dict['date'] = precip_last_12_months[rec][0]
        tobs_dict['temp'] = precip_last_12_months[rec][2]
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return the json list of all stations in the data set"""
    all_stations = session.query(Station.station, Station.name).all()




    stations_data = []
    for rec in range(len(all_stations)):
        station_dict = {}
        station_dict['station_id'] = all_stations[rec][0]
        station_dict['name'] = all_stations[rec][1]
        stations_data.append(station_dict)

    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the json list of tobs for the last 12 months"""
    last12_tobs = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
               filter(Measurement.date.between('2016-01-16', '2017-01-15')).\
               group_by(Measurement.date).order_by(Measurement.date).all()

    # tobs_df = pd.DataFrame(last12_tobs, columns = ['date', 'station', 'tobs'])[0:]
    tobs_data = []
    for rec in range(len(last12_tobs)):
        tobs_dict = {}
        tobs_dict['date'] = last12_tobs[rec][0]
        tobs_dict['temp'] = last12_tobs[rec][2]
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def temp_range(start):
    """Return the json list of min, average and max temperature for a given date"""
    min_temp = session.query(func.min(Measurement.tobs)).\
               filter(Measurement.date == start).first()
    avg_temp = session.query(func.avg(Measurement.tobs)).\
               filter(Measurement.date == start).first()
    max_temp = session.query(func.max(Measurement.tobs)).\
               filter(Measurement.date == start).first()

    tobs_data = [min_temp, avg_temp, max_temp]
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>/<end_date>")
def temp_ranges(start, end_date):
    """Return the json list of min, average and max temperature for a given date range"""
    min_temp = session.query(func.min(Measurement.tobs)).\
               filter(Measurement.date.between(start, end_date)).first()
    avg_temp = session.query(func.avg(Measurement.tobs)).\
               filter(Measurement.date.between(start, end_date)).first()
    max_temp = session.query(func.max(Measurement.tobs)).\
               filter(Measurement.date.between(start, end_date)).first()

    tobs_data = [min_temp, avg_temp, max_temp]
    return jsonify(tobs_data)


if __name__ == "__main__":
    app.run(debug=False)
