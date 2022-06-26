import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('NOAA_data.sqlite')
cur = conn.cursor()

cur.execute('SELECT timestamp, airtemp FROM data ORDER BY timestamp')
dates = list()
temps = list()
for row in cur :
    dates.append(row[0])
    temps.append(row[1])

# Plot scatter

plt.scatter(dates, temps)

# Labelling

plt.xlabel("Date")
plt.ylabel("Temp in Faherenheit")

# Auto space
plt.tight_layout()

# Display
plt.show()
