from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import ssl
import xml.etree.ElementTree as ET
import sqlite3

#connect to sql database
conn = sqlite3.connect('NOAA_data.sqlite')
cur = conn.cursor()

#get the current day month and year
today = date.today()
date = today.timetuple()
current_day = date[2]
current_month = date[1]
current_year = date[0]

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#call NOAA observatory website and parse using BeautifulSoup
url = 'https://w1.weather.gov/data/obhistory/KMSP.html'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the tr tags
tags = soup('tr')


#create a count variable for printing
countvar = 0

header = ['Date: ', 'Time (cdt): ', 'Wind (mph): ', 'Vis. (mi.): ', 'Weather: ', 'Sky Cond.: ', 'Air Temperature (ºF): ', 'Dewpoint: ', '', '6 Hour Max Temp (ºF): ', '6 Hour Min Temp (ºF): ', 'Relative Humidity: ', 'Wind Chill (ºF): ', 'Heat Index (ºF): ', 'Pressure Altimeter (in): ', 'Pressure Sea Level (mb): ', '1 hr. Precipitation (in): ', '3 hr. Precipitation (in): ', '6 hr. Precipitation (in): ']
print(len(header))

#for loop over tr tags on NOAA observatory website
for tag in tags:
    #observatory data begins at 7
    if countvar > 6:
        #using this to only print a few timepoints
        #if countvar > 15:
        #    break

        a = repr(tag)
        b=a.split()

        #this breaks the loop when the observatory timepoints are done being read
        if len(a) > 400:
            break

        #printout heading
        print('\n')
        print('========== ',countvar,' ==========')


        #create empty list to store variable data
        lst = list()
        for i in range(19):
            lst.append('NA')

        #variable for looping through html child contents (start at -1 to being at index = 0)
        dumvar = -1

        #loop through each measured variable in html child contents and place into lst
        for child in tag:
            dumvar = dumvar + 1
            #convert soup object to string using repr()
            childvar = repr(child)
            #try except loop to see if there is a html value in the tag. if not, 'NA' is put into lst
            try:
                start = childvar.index('>')
                end = childvar.index('<', start+1)
                substring = childvar[start+1:end]
                if dumvar == 11:
                    toss = substring.split('%')
                    substring = toss[0]
                #check to see if the value extracted is a real value or an empty tag. if empty, 'NA' placed into lst
                if len(substring) > 0:
                    lst[dumvar] = substring
                else:
                    lst[dumvar] = 'NA'
                #if len(substring) > 0:
                #    print(header[dumvar], substring)
            except:
                lst[dumvar] = 'NA'
                continue

        #calcuate date and month combination, accounting for changes that happen at beginning of new months and new years
        if current_day < 4:
            if str(lst[0]) > 20:
                if current_month == 1:
                    month = 12
                    year = current_year - 1
                else:
                    month = current_month - 1
        else:
            day = int(lst[0])
            month = current_month
            year = current_year
        #calculate the time from the string value
        time = lst[1].split(':')
        #create datetime value
        timepoint = datetime(year, month, day, int(time[0]), int(time[1]))
        #print date & time, then print the list of measurements
        print(timepoint)
        print(type(timepoint))
        print(lst)


        #check if this timepoint already exists
        cur.execute('SELECT timestamp FROM data WHERE timestamp = ? ', (timepoint,))
        row = cur.fetchone()
        if row is None:
            #store new measurement data in database
            cur.execute('''INSERT OR IGNORE INTO data (timestamp, windmph, vis, weather, skycond, airtemp, dewpoint, sixhrmax, sixhrmin, relhum, windchill, heatindex, p_alt, p_sea, onehrprecip, threehrprecip, sixhourprecip)
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', ( timepoint,  lst[2],  lst[3],  lst[4],  lst[5],  lst[6], lst[7], lst[9], lst[10], lst[11], lst[12], lst[13], lst[14], lst[15], lst[16], lst[17], lst[18]) )

        conn.commit()
    #iterate to next timepoint
    countvar = countvar + 1

cur.close()
