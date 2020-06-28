"""db utils"""

import os
import sqlite3

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'temperature_database.db')


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def db_first_time_setup():
    con = db_connect()
    cur = con.cursor()
    hive_table = ("CREATE TABLE HiveThermostat(\n"
                  "    id integer PRIMARY KEY,\n"
                  "    date_time text NOT NULL,\n"
                  "    temperature text NOT NULL)")
    cur.execute(hive_table)


def db_setup_tables():
    pass


