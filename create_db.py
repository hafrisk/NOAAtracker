import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('NOAA_data.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''

CREATE TABLE data (
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    timestamp       TIME,
    windmph         INTEGER,
    vis             INTEGER,
    weather         TEXT,
    skycond         TEXT,
    airtemp         INTEGER,
    dewpoint        INTEGER,
    sixhrmax        INTEGER,
    sixhrmin        INTEGER,
    relhum          INTEGER,
    windchill       INTEGER,
    heatindex       INTEGER,
    p_alt           INTEGER,
    p_sea           INTEGER,
    onehrprecip     INTEGER,
    threehrprecip   INTEGER,
    sixhourprecip   INTEGER

);
''')
