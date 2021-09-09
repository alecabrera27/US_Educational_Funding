# Dependencies
import numpy as np
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
# get the database credentials
import config

# create database engine
db_url = f"postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
engine = create_engine(db_url)

# drop the RawRecord table if it already exists
try:
    with engine.connect() as con:

        rs = con.execute(text('DROP TABLE "RawRecords";'))
except:
    print("drop table failed")



df = pd.read_csv("Resources/states_all.csv")

base_df = df[['PRIMARY_KEY', 
              'STATE', 
              'YEAR',
              'ENROLL',
              'TOTAL_REVENUE', 
              'FEDERAL_REVENUE', 
              'STATE_REVENUE', 
              'LOCAL_REVENUE',
              'TOTAL_EXPENDITURE',
              'INSTRUCTION_EXPENDITURE', 
              'SUPPORT_SERVICES_EXPENDITURE',
              'OTHER_EXPENDITURE',
              'CAPITAL_OUTLAY_EXPENDITURE',
              'AVG_MATH_4_SCORE',
              'AVG_MATH_8_SCORE',
              'AVG_READING_4_SCORE',
              'AVG_READING_8_SCORE'
             ]]

clean_df = base_df.dropna()

# rename the columns to match our schema
base_table = clean_df.rename(columns = {
    'PRIMARY_KEY':'Id', 
    'STATE':'State', 
    'YEAR':'Year',
    'ENROLL':'Enrolled',
    'TOTAL_REVENUE':'TotalRevenue', 
    'FEDERAL_REVENUE':'FederalRevenue',
    'STATE_REVENUE':'StateRevenue',
    'LOCAL_REVENUE':'LocalRevenue',
    'TOTAL_EXPENDITURE':'TotalExpenditure',
    'INSTRUCTION_EXPENDITURE':'InstructionExpenditure',
    'SUPPORT_SERVICES_EXPENDITURE':'SupportServicesExpenditure',
    'CAPITAL_OUTLAY_EXPENDITURE':'CapitalOutlayExpenditure',
    'OTHER_EXPENDITURE':'OtherExpenditure',
    'AVG_MATH_4_SCORE':'AvgMath4Score',
    'AVG_MATH_8_SCORE':'AvgMath8Score',
    'AVG_READING_4_SCORE':'AvgReading4Score',
    'AVG_READING_8_SCORE':'AvgReading8Score'
})


# store base_table in the database
con = engine.connect()
table_name = 'RawRecords'
base_table.to_sql(table_name, con, index=False)





