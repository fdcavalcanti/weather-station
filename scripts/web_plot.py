import base64
from io import BytesIO
from pathlib import Path

from flask import Flask
from datetime import datetime, timedelta

from plot_history import WeatherStationDB, PlotWeatherStation

PLOT_DAYS_PREVIOUS = 4
TIME_DELTA = timedelta(days = PLOT_DAYS_PREVIOUS)
DATABASE_PATH = Path(__file__).parents[1] / "database" / "station.db"
print(f"Database: {DATABASE_PATH}")

app = Flask(__name__)


@app.route("/")
def show_plot():
    datetime_days_ago = datetime.now() - TIME_DELTA
    station_db = WeatherStationDB(DATABASE_PATH)
    start_date = datetime.strftime(datetime_days_ago, "%Y-%m-%d")  
    station_db.set_start_date(start_date)

    temp_bmp = station_db.read_temperature_bmp280()
    temp_dht = station_db.read_temperature_dht22()
    humidity = station_db.read_humidity()
    press = station_db.read_pressure()

    plot_tool = PlotWeatherStation()
    plot_tool.add_measurement(temp_bmp)
    plot_tool.add_measurement(temp_dht)
    plot_tool.add_measurement(humidity)
    plot_tool.add_measurement(press)
    plot_tool.refresh_plot()

    buf = BytesIO()
    plot_tool.fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
