"""db utils"""

import os
import sqlite3

# create a default path to connect to and create (if necessary) a database
# called 'temperature_database.db' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'temperature_database.db')


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def db_first_time_setup():
    con = db_connect()
    cursor = con.cursor()
    db_setup_tables(cursor)


def db_setup_tables(cursor):
    hive_table = ("CREATE TABLE HiveThermostat(\n"
                  "    id integer PRIMARY KEY,\n"
                  "    date_time text NOT NULL,\n"
                  "    temperature text NOT NULL)")
    cursor.execute(hive_table)


def _create_measurement(con, date_time, temperature):
    sql = "INSERT INTO HiveThermostat (date_time, temperature) VALUES (?, ?)"
    cur = con.cursor()
    cur.execute(sql, (date_time, temperature))
    con.commit()


def store_measurement(date_time, temperature):
    con = db_connect()
    _create_measurement(con, date_time, temperature)
    con.close()


def get_all_measurements():
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM HiveThermostat ORDER BY date_time")
    results = cur.fetchall()
    con.close()
    return results
