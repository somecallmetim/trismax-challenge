import csv
import os
import urllib3
import requests
import config
import pymysql

db = pymysql.connect(   host = "localhost",
                        user = config.username,
                        passwd = config.password,
                        db = config.dbName)
cursor = db.cursor()
cursor.close()

http = urllib3.PoolManager()

url = "http://winterolympicsmedals.com/medals.csv"
rawCSVFile = http.request('GET', url)
# print(rawCSVFile.status)
# print(rawCSVFile.data)
# csvReader = csv.reader(rawCSVFile)

# lines = len(list(csvReader))
# print(lines)

# rawCSVFile.data is a member of the bytes class (essentially a string of bytes)
	# map takes the built in chr function and applies it to each byte in data
	# and gives you back a map object. A map object is iterable, so you can
	# use the join function to convert it into a string
	# TLDR the data is converted to a regular good old fashioned string
data = "".join(map(chr, rawCSVFile.data))
# convert data into a list
data = data.split('\n')



i = 0

for row in data:
	print(row)
	print(i)
	i += 1
	if i > 9:
		break


def downloadCsv():
	pass

def parseCsv():
	pass

# rawDataFile = os.path.isfile('./data.csv')
#
# if rawDataFile:
	