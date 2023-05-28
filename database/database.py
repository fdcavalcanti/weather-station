from dataclasses import dataclass
from pathlib import Path
import os
import sqlite3


@dataclass
class Measurement:
    """Measurement data."""
    timestamp: str
    temperature: float
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
    conn = sqlite3.connect(database)
    conn.execute(f"INSERT INTO weather_log (datetime,temperature,pressure,humidity) \
        VALUES ({meas.timestamp}, {meas.temperature}, {meas.pressure}, {meas.humidity})")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    db_path = "/home/rasp/weather-station/database/station.db"
    try:
        db_path = create_database("/home/rasp/weather-station/database/db_schema.sqlite", "station")
    except FileExistsError:
        pass
    aaa = Measurement("12342003030", 29.5, 1009.3, 70.1)
    add_reading_to_database(db_path, aaa)
