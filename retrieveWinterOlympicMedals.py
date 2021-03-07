import urllib3
import config
import pymysql

db = pymysql.connect(host="localhost",
                     user=config.username,
                     passwd=config.password,
                     db=config.dbName)
cursor = db.cursor()
cursor.close()

def getListOfCSVEntries():
    http = urllib3.PoolManager()
    url = "http://winterolympicsmedals.com/medals.csv"
    httpResponse = http.request('GET', url)

    # this is data that will purposely fail our test parameters to make sure our csv validation works properly
    badData = [
        ['1908', 'Chamonix', 'Skating', 'Figure skating', 'AUT', 'individual', 'M', 'Silver'],
        ['1924', '', 'Skating', 'Figure skating', 'AUT', 'individual', 'W', 'Gold'],
        ['1924', 'Chamonix', '', 'Figure skating', 'AUT', 'pairs', 'X', 'Gold'],
        ['1924', 'Chamonix', 'Bobsleigh', '', 'BEL', 'four-man', 'M', 'Bronze'],
        ['1924', 'Chamonix', 'Ice Hockey', 'Ice Hockey', '', 'ice hockey', 'M', 'Gold'],
        ['1924', 'Chamonix', 'Biathlon', 'Biathlon', 'FINLAND', 'military patrol', 'M', 'Silver'],
        ['1924', 'Chamonix', 'Skating', 'Figure skating', 'FIN', '', 'X', 'Silver'],
        ['1924', 'Chamonix', 'Skating', 'Speed skating', 'FIN', '10000m', 'V', 'Heavy'],
        ['1924', 'Chamonix', 'Skating', 'Speed skating', 'FIN', '10000m', 'M', 'Silver', 'test'],
        ['1924', 'Chamonix', 'Skating', 'Speed skating', 'FIN', '10000m', 'M']
    ]

    # httpResponse.data is a member of the bytes class (essentially a string of bytes)
        # map takes the python built in chr function and applies it to each byte in data
        # and gives you back a map object. A map object is iterable, so you can
        # use the join function to convert it into a string
        # TLDR the data is converted to a regular good old fashioned string
    listOfData = "".join(map(chr, httpResponse.data))

    # convert listOfData into a list of strings
    listOfData = listOfData.split('\n')

    # convert listOfData into a list of lists, where each sublist represents a potential db entry
    for i in range(len(listOfData )):
        listOfData[i] = listOfData[i].split(",")
    return badData + listOfData

i = 0
listOfEntries = getListOfCSVEntries()

# prints first 10 rows of of the
for row in listOfEntries:
    print(row)
    i += 1
    if i > 19:
        break
