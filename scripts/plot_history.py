import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field

DB_PATH = Path(__file__).parents[1] / "database" / "station.db"


class MeasurementType(Enum):
    TEMPERATURE_DHT22 = "temperature_dht22"
    TEMPERATURE_BMP280 = "temperature_bmp280"
    REL_HUMIDITY = "humidity"
    ATM_PRESSURE = "pressure"
    DATE_TIME = "datetime"


@dataclass
class Measurement:
    db_data: list
    meas_type: MeasurementType = field(init=False)
    measurement: list = field(init=False)
    date_time: list = field(init=False)

    def __post_init__(self):
        columns = self.db_data[0]
        for measurement in MeasurementType:
            if columns[1] == measurement.value:
                self.meas_type = measurement
                break

        self.date_time = [datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S") for item in self.db_data[1:]]
        self.measurement = [item[1] for item in self.db_data[1:]]


def get_columns_from_db(columns: tuple) -> list:
    """Tuple containing column names to be retrieved."""
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    columns = ",".join(columns)
    cursor.execute(f"SELECT {columns} FROM weather_log")
    data = cursor.fetchall()
    con.close()
    return data


def read_temperature_dht22_from_db() -> list:
    """Get all available temperature data from the DB."""
    columns = (MeasurementType.DATE_TIME.value,
               MeasurementType.TEMPERATURE_DHT22.value)
    data = get_columns_from_db(columns)
    data.insert(0, columns)

    return data


def read_temperature_bmp280_from_db() -> list:
    """Get all available temperature data from the DB."""
    columns = (MeasurementType.DATE_TIME.value,
               MeasurementType.TEMPERATURE_BMP280.value)
    data = get_columns_from_db(columns)
    data.insert(0, columns)

    return data


def read_pressure_from_db() -> list:
    """Get all available atmospheric pressure values from the DB."""
    columns = (MeasurementType.DATE_TIME.value,
               MeasurementType.ATM_PRESSURE.value)
    data = get_columns_from_db(columns)
    data.insert(0, columns)

    return data


def read_humidity_from_db() -> list:
    """Get all available humidity values from the DB."""
    columns = (MeasurementType.DATE_TIME.value,
               MeasurementType.REL_HUMIDITY.value)
    data = get_columns_from_db(columns)
    data.insert(0, columns)

    return data


def plot_history(data: list):
    columns = data[0]
    number_of_measurements = len(columns) - 1
    datetime_list = [datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S") for item in data[1:]]
    column_data = []
    for idx in range(1, number_of_measurements + 1):
        meas = [item[idx] for item in data[1:]]
        column_data.append(meas)

    fig, ax = plt.subplots()
    for idx, sensor_data in enumerate(column_data):
        ax.plot(datetime_list, sensor_data, label=columns[idx+1])
        ax.legend()
    plt.show()


class PlotWeatherStation:
    """Plots weather station data on the same time period."""
    def __init__(self):
        self.fig, self.ax = plt.subplots(nrows=3)
        self.measurement_list = []
    
    def add_measurement(self, meas_data: Measurement):
        self.measurement_list.append(meas_data)

    def refresh_plot(self):
        for idx, data in enumerate(self.measurement_list):
            if data.meas_type in (MeasurementType.TEMPERATURE_BMP280, MeasurementType.TEMPERATURE_DHT22):
                axis = 0
            if data.meas_type == MeasurementType.ATM_PRESSURE:
                axis = 1
            if data.meas_type == MeasurementType.REL_HUMIDITY:
                axis = 2

            self.ax[axis].plot(data.date_time,
                               data.measurement,
                               label=data.meas_type.value)
            self.ax[axis].legend()
        plt.show()

if __name__ == "__main__":
    print(f"Database path: {DB_PATH}")
    temp_bmp = Measurement(read_temperature_bmp280_from_db())
    temp_dht = Measurement(read_temperature_dht22_from_db())
    humi = Measurement(read_humidity_from_db())
    press = Measurement(read_pressure_from_db())
    aa = PlotWeatherStation()
    aa.add_measurement(temp_bmp)
    aa.add_measurement(temp_dht)
    aa.add_measurement(humi)
    aa.add_measurement(press)
    aa.refresh_plot()
