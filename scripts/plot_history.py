import argparse
import sqlite3
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
from datetime import datetime, time
from enum import Enum
from dataclasses import dataclass, field


parser = argparse.ArgumentParser(description="Visualize weather station data")
parser.add_argument("--start",
                    action="store",
                    default=None,
                    required=False,
                    type=str,
                    help="Start date to query in format: YYYY-MM-DD")
parser.add_argument("--end",
                    action="store",
                    default=None,
                    required=False,
                    type=str,
                    help="Final date to query in format: YYYY-MM-DD")
parser.add_argument("--db",
                    action="store",
                    required=False,
                    default=Path(__file__).parents[1] / "database" / "station.db",
                    help="Path to database file")


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


class WeatherStationDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.start_date = "2023-01-01 00:00:00"
        self.end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def read_temperature_dht22(self) -> list:
        """Get all available temperature data from the DB.
        
        Returns:
            Measurement: dataclass with DHT22 temperature data.    
        """
        columns = (MeasurementType.DATE_TIME.value,
                   MeasurementType.TEMPERATURE_DHT22.value)
        data = self.__get_columns_from_db(columns)
        data.insert(0, columns)

        return Measurement(data)

    def read_temperature_bmp280(self) -> list:
        """Get all available temperature data from the DB.

        Returns:
            Measurement: dataclass with BMP280 temperature data.    
        """
        columns = (MeasurementType.DATE_TIME.value,
                MeasurementType.TEMPERATURE_BMP280.value)
        data = self.__get_columns_from_db(columns)
        data.insert(0, columns)

        return Measurement(data)

    def read_pressure(self) -> list:
        """Get all available atmospheric pressure values from the DB.

        Returns:
            Measurement: dataclass with BMP280 pressure data.    
        """
        columns = (MeasurementType.DATE_TIME.value,
                MeasurementType.ATM_PRESSURE.value)
        data = self.__get_columns_from_db(columns)
        data.insert(0, columns)

        return Measurement(data)

    def read_humidity(self) -> list:
        """Get all available humidity values from the DB.

        Returns:
            Measurement: dataclass with DHT22 humidity data.    
        """
        columns = (MeasurementType.DATE_TIME.value,
                MeasurementType.REL_HUMIDITY.value)
        data = self.__get_columns_from_db(columns)
        data.insert(0, columns)

        return Measurement(data)

    def set_start_date(self, date: str):
        """Set start date for query.

        Args:
            date (str): date in format YYYY-MM-DD.
        """
        start_date = self.__validate_date_format(date)
        self.start_date = self.__append_time(start_date)

    def set_end_date(self, date: str):
        """Set end date for query.

        Args:
            date (str): date in format YYYY-MM-DD.
        """
        end_date = self.__validate_date_format(date)
        self.end_date = self.__append_time(end_date)
        

    def __append_time(self, date: str):
        """Set time to 00:00:00"""
        return date + " 00:00:01"

    def __validate_date_format(self, date):
        try:
            _ = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid datetime format")
            raise
        return date

    def __get_columns_from_db(self,
                              columns: tuple) -> list:
        """Tuple containing column names to be retrieved."""
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        columns = ",".join(columns)
        query_cmd = f"""
                    SELECT {columns}
                    FROM weather_log
                    WHERE {MeasurementType.DATE_TIME.value}
                    BETWEEN '{self.start_date}'
                    AND '{self.end_date}'
                    """
        print(f"Query: {query_cmd}")
        cursor.execute(query_cmd)
        data = cursor.fetchall()
        con.close()
        return data


class PlotWeatherStation:
    """Plots weather station data on the same time period."""
    nighttime = time(18,0,0)
    daytime = time(6,0,0)

    def __init__(self):
        self.fig, self.ax = plt.subplots(nrows=3, sharex=True)
        self.measurement_list = []
    
    def add_measurement(self, meas_data: Measurement):
        self.measurement_list.append(meas_data)

    def refresh_plot(self):
        for data in self.measurement_list:
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
            self.ax[axis].grid(True)
        
    def show(self):
        plt.show()


if __name__ == "__main__":
    args = parser.parse_args()
    print(f"Database path: {args.db}")

    if args.start:
        try:
            datetime.strptime(args.start, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format!")
            sys.exit(1)

    if args.end:
        try:
            datetime.strptime(args.end, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format!")
            sys.exit(1)

    if not os.path.isfile(args.db):
        print("Database file not found!")
        sys.exit(1)

    dbtool = WeatherStationDB(args.db)
    if args.start:
        dbtool.set_start_date(args.start)
    if args.end:
        dbtool.set_end_date(args.end)

    temp_bmp = dbtool.read_temperature_bmp280()
    temp_dht = dbtool.read_temperature_dht22()
    humi = dbtool.read_humidity()
    press = dbtool.read_pressure()
    plot_tool = PlotWeatherStation()
    plot_tool.add_measurement(temp_bmp)
    plot_tool.add_measurement(temp_dht)
    plot_tool.add_measurement(humi)
    plot_tool.add_measurement(press)
    plot_tool.refresh_plot()
    plot_tool.show()
