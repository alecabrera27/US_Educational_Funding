# Dependencies
import numpy as np
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
# import the database credentials
import config

# create database engine
db_url = f"postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
engine = create_engine(db_url)


# load all the raw data into a datafame
query = text('''SELECT * FROM "RawRecords";''')
df = pd.read_sql_query(query,con=engine, index_col='Id')


# create a df for the stats with the same index as the raw data
stats_df = pd.DataFrame(index=df.index)
# rename the index to match the schema
stats_df.index.rename('RecordId', inplace=True)

# calculate the stats
stats_df['FederalFundingPercent'] = df['FederalRevenue']/df['TotalRevenue']
stats_df['StateFundingPercent'] = df['StateRevenue']/df['TotalRevenue']
stats_df['LocalFundingPercent'] = df['LocalRevenue']/df['TotalRevenue']
stats_df['RevenuePerStudent'] = df['TotalRevenue']/df['Enrolled']
stats_df['InstructionalExpensePercent'] = df['InstructionExpenditure']/df['TotalRevenue']


# drop the RawRecord table if it already exists
try:
    with engine.connect() as con:

        rs = con.execute(text('DROP TABLE "CalculatedStats";'))
except:
    print("drop table failed")


# store in the database
con = engine.connect()
table_name = 'CalculatedStats'
stats_df.to_sql(table_name, con)





