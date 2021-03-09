import config
import pymysql
import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation, InListValidation

db = pymysql.connect(host="localhost",
                     user=config.username,
                     passwd=config.password,
                     db=config.dbName)
cursor = db.cursor()
cursor.close()

# get the csv file and convert it to pandas's DataFrame data type
def getPdDataFrame():
    url = "http://winterolympicsmedals.com/medals.csv"
    return pd.read_csv(url)

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
        Column('Event gender', [InListValidation(['M', 'W', 'X'])], allow_empty=False),
        Column('Medal', [InListValidation(['Gold', 'Silver', 'Bronze'])], allow_empty=False),
    ])

    # passes DataFrame to pandas_schema and validates the data based on the parameters we've already set
    errorsList = schema.validate(pdDataFrame)

    # if there are errors, remove them from the data then save the data as a new csv
    if errorsList:
        errorsListIndexRows = [e.row for e in errorsList]
        pdCleanDataFrame = pdDataFrame.drop(index=errorsListIndexRows)
        pdCleanDataFrame.to_csv('cleanData.csv')
    else:
        pdDataFrame.to_csv('cleanData.csv')

pdDataFrame = getPdDataFrame()
validateData(pdDataFrame)