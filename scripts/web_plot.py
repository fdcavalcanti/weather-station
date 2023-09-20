import base64
from io import BytesIO
from pathlib import Path

from flask import Flask
from matplotlib.figure import Figure
from datetime import datetime, timedelta

from plot_history import WeatherStationDB, Measurement

PLOT_DAYS_PREVIOUS = 2
TIME_DELTA = timedelta(days = PLOT_DAYS_PREVIOUS)
DATABASE_PATH = Path(__file__).parents[0] / "database" / "station.db"

app = Flask(__name__)


@app.route("/")
def show_plot():
    datetime_days_ago = datetime.now() - TIME_DELTA
    station_db = WeatherStationDB(DATABASE_PATH)
    station_db.set_start_date(datetime.strptime(datetime_days_ago, "%Y-%m-%d"))

    temp_bmp = Measurement(station_db.read_temperature_bmp280())
    temp_dht = Measurement(station_db.read_temperature_dht22())
    humidity = Measurement(station_db.read_humidity())
    press = Measurement(station_db.read_pressure())

    fig = Figure()
    ax = fig.subplots(nrows=3)
    ax[0].plot(temp_bmp.date_time, temp_bmp.measurement, label=temp_bmp.meas_type.value)
    ax[0].plot(temp_dht.date_time, temp_dht.measurement, label=temp_dht.meas_type.value)
    ax[1].plot(humidity.date_time, humidity.measurement, label=humidity.meas_type.value)
    ax[2].plot(press.date_time, press.measurement, label=press.meas_type.value)

    for idx in [1,2,3]:
        ax[idx].legend()
        ax[idx].grid(True)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
