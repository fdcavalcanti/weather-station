from dataclasses import dataclass
from pathlib import Path
import os
import sqlite3


@dataclass
class Measurement:
    """Measurement data."""
    timestamp: str
    temperature_bmp280: float
    temperature_dht22: float
    pressure: float
    humidity: float


def create_database(schema: os.PathLike, name: str) -> os.PathLike:
    """Creates a database based on current schema.

    Args:
        schema: Path to the schema file.
        name: name of the database file.

    Returns:
        Path to the created database file.    
    """
    schema = Path(schema)
    if not schema.exists():
        raise FileNotFoundError(f"Schema file not found: {schema}")

    db_path = schema.parents[0] / (name + ".db")
    if db_path.exists():
        raise FileExistsError(f"Database already exists: {db_path}")
    print(f"Creating database in: {db_path}")

    with open(schema, "r", encoding="utf-8") as schema_file:
        schema_str = schema_file.read()

    conn = sqlite3.connect(db_path)
    conn.execute(schema_str)
    conn.commit()
    conn.close()
    return db_path


def add_reading_to_database(database: os.PathLike, meas: Measurement) -> None:
    """Adds a measurement to the database.
    
    Args:
        database: path to the .db file.
        meas: measurement dataclass.

    Returns:
        None
    """
    db = sqlite3.connect(database)
    command = f"INSERT INTO weather_log (datetime,temperature_bmp280,temperature_dht22,pressure,humidity) \
    VALUES (?,?,?,?,?);"
    cur = db.cursor()
    cur.execute(command, (meas.timestamp, meas.temperature_bmp280,
                          meas.temperature_dht22, meas.pressure, meas.humidity))
    db.commit()
    db.close()


#if __name__ == "__main__":
#    db_path = "/home/rasp/weather-station/database/station.db"
#    try:
#        db_path = create_database("/home/rasp/weather-station/database/db_schema.sqlite", "station")
#    except FileExistsError:
#        pass
    #aaa = Measurement("12342003030", 29.5, 1009.3, 70.1)
    #add_reading_to_database(db_path, aaa)
