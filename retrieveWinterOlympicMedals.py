import config
from sqlalchemy import create_engine
import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation, InListValidation
import requests

# get the csv file and convert it to pandas's DataFrame data type
def getPdDataFrame():
    url = "http://winterolympicsmedals.com/medals.csv"
    pdDataFrame = pd.read_csv(url)
    # this fixes issues caused by the fact that one of the columns in the csv file has two words
        # separated by a white space by forcing these specific column names to be used
    pdDataFrame.columns = ['Year', 'City', 'Sport', 'Discipline', 'NOC', 'Event', 'Gender', 'Medal']
    return pdDataFrame

# validate the data in the DataFrame (from the csv file)
def validateData(pdDataFrame):
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
        # print errors in data entry that occurred
        for e in errorsList:
            print(e)
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
def sendBackCleanData():
    # dummy url for testing purposes
    url = "https://httpbin.org/post"
    # opens csv, creates http request, and sends it to specified url
    with open('cleanData.csv', 'r') as cleanData:
        r = requests.post(url, files={'cleanData.csv': cleanData})
        print(r)
        # return r so we can check and respond to various server responses
        return r

pdDataFrame = getPdDataFrame()
pdDataFrame = validateData(pdDataFrame)
sendBackCleanData()

# persists clean data into mysql database
engine = create_engine('mysql+pymysql://'
                       + config.username + ':' + config.password + '@localhost/' + config.dbName)
# creates table if doesn't exist, replaces table if it does exist
pdDataFrame.to_sql('winterOlympics', engine, if_exists='replace', index=False)