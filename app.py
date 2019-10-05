import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome the cool weather API"


@app.route("/precipitation")
def precipitation():
    session = Session(engine)
    results = session.execute("SELECT * FROM measurement")
    dict_ = {}
    for r in results:
        x = r[2]
        y = r[3]
        dict_[x] = y
    return jsonify(dict_)


@app.route("/stations")
def stations():
    session = Session(engine)
    results = session.execute("SELECT station FROM measurement")
    stations_ = []
    for r in results:
        stations_.append(r)
    return jsonify(stations_)


@app.route("/tobs")
def tobs():
    session = Session(engine)
    most_repeated_station = session.execute(
        "SELECT * FROM measurement WHERE station = 'USC00519281' AND date > '2016-09-01';")
    most_repeated_station_12_months = []
    for m in most_repeated_station:
        most_repeated_station_12_months.append(m[4])
    return jsonify(most_repeated_station_12_months)


@app.route("/<start>/<end>")
def calc_temps(start_date, end_date):
    session = Session(engine)
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).
                   filter(Measurement.date >= start_date).filter(
        Measurement.date <= end_date).all())


if __name__ == '__main__':
    app.run(debug=True)
