import config
from sqlalchemy import create_engine
import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation, InListValidation
import requests
import datetime


# get the csv file and convert it to pandas's DataFrame data type
def getCSVFile():
    url = "http://winterolympicsmedals.com/medals.csv"
    pdDataFrame = pd.read_csv(url)
    # this fixes issues caused by the fact that one of the columns in the csv file has two words
        # separated by a white space by forcing these specific column names to be used
    pdDataFrame.columns = ['Year', 'City', 'Sport', 'Discipline', 'NOC', 'Event', 'Gender', 'Medal']
    return pdDataFrame


# validate the data in the DataFrame (from the csv file)
def validateData(pdDataFrame, logFileName):
    # this tells pandas_schema what the data should look like
    schema = Schema([
        Column('Year', [InRangeValidation(1924, 2020)], allow_empty=False),
        Column('City', allow_empty=False),
        Column('Sport', allow_empty=False),
        Column('Discipline', allow_empty=False),
        Column('NOC', allow_empty=False),
        Column('Event', allow_empty=False),
        Column('Gender', [InListValidation(['M', 'W', 'X'])], allow_empty=False),
        Column('Medal', [InListValidation(['Gold', 'Silver', 'Bronze'])], allow_empty=False),
    ])

    # passes DataFrame to pandas_schema and validates the data based on the parameters we've already set
    errorsList = schema.validate(pdDataFrame)

    # if there are errors, remove them from the data then save the data as a new csv
    if errorsList:
        logFile = open("./logs/" + logFileName, "a+")
        logFile.write("list of errors concerning submitted data\n---------------")
        # print errors in data entry that occurred
        for e in errorsList:
            logFile.write(e)
            print(e)
        logFile.close()
        # gets the indexes of the bad data (list comprehension)
        errorsListIndexRows = [e.row for e in errorsList]
        # drops the bad data and gives you a new DataFrame with only clean data
        pdCleanDataFrame = pdDataFrame.drop(index=errorsListIndexRows)
        # converts clean data to csv to later send to stake holders
        pdCleanDataFrame.to_csv('cleanData.csv')
        return pdCleanDataFrame
    else:
        # converts clean data to csv to later send to stake holders
        pdDataFrame.to_csv('cleanData.csv')
        return pdDataFrame


# send clean csv back to client
def sendBackCleanData(logFileNmae):
    # dummy url for testing purposes
    url = "https://httpbin.org/post"
    # opens csv, creates http request, and sends it to specified url
    with open('cleanData.csv', 'r') as cleanData:
        response = requests.post(url, files={'cleanData.csv': cleanData})
        logFile = open("./logs/" + logFileName, "a+")
        logFile.write("status code for the csv we sent to client: " + str(response.status_code))
        print(response.status_code)
        # return response so we can check and respond to various server responses
        return response

def findSQLEntriesByNocMedalAndYear(dbEngine, noc, medal, year):
    noc = "'" + noc + "'"
    medal = "'" + medal + "'"
    with dbEngine.connect() as dbConnection:
        sqlQuery = 'SELECT * FROM winterOlympics WHERE noc = {} AND medal = {} AND year = {}'.format(noc, medal, year)
        dbResponse = dbConnection.execute(sqlQuery)
        for row in dbResponse:
            print(row)


now = str(datetime.datetime.now().replace(microsecond=0))
logFileName = 'logFile: ' + now

pdDataFrame = getCSVFile()
pdDataFrame = validateData(pdDataFrame, logFileName)
httpResponse = sendBackCleanData(logFileName)

# persists clean data into mysql database
engine = create_engine('mysql+pymysql://'
                       + config.username + ':' + config.password + '@localhost/' + config.dbName)
# creates table if doesn't exist, replaces table if it does exist
pdDataFrame.to_sql('winterOlympics', engine, if_exists='replace', index=False)

findSQLEntriesByNocMedalAndYear(engine, 'usa', 'gold', 2006)
