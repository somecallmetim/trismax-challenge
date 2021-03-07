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

    # httpResponse.data is a member of the bytes class (essentially a string of bytes)
        # map takes the python built in chr function and applies it to each byte in data
        # and gives you back a map object. A map object is iterable, so you can
        # use the join function to convert it into a string
        # TLDR the data is converted to a regular good old fashioned string
    listOfData = "".join(map(chr, httpResponse.data))

    # convert listOfData into a list
    listOfData = listOfData.split('\n')
    return listOfData

i = 0
listOfEntries = getListOfCSVEntries()

# prints first 10 rows of of the
for row in listOfEntries:
    print(row)
    i += 1
    if i > 9:
        break
