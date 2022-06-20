from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

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


#for loop over tr tags on NOAA observatory website
for tag in tags:
    #header info is contained in 4
    if countvar == 4:
        print('\n')
        print('========== 4 ==========')
        print(repr(tag))

        #convert to string using repr()
        a = repr(tag)
        print(len(a))
        b=a.split()
        print(len(b))

        for child in tag:
            print(child)

    #observatory data begins at 7
    if countvar > 6:
        #using this to only print a few timepoints
        if countvar > 15:
            break

        a = repr(tag)
        b=a.split()

        #this breaks the loop when the observatory timepoints are done being read
        if len(a) > 400:
            break

        print('\n')
        print('========== ',countvar,' ==========')
        print(repr(tag))
        print(len(a))
        print(len(b))

        print('\n')
        print('========== ',countvar,' ==========')
        dumvar = -1
        for child in tag:
            dumvar = dumvar + 1
            #print(child)
            childvar = repr(child)
            try:
                start = childvar.index('>')
                end = childvar.index('<', start+1)
                substring = childvar[start+1:end]
                if len(substring) > 0:
                    print(header[dumvar], substring)
            except:
                continue
    countvar = countvar + 1

#for child in tags[4].contents:
#    print(child)
