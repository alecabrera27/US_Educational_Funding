import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

import config


# create database engine
db_url = f"postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
engine = create_engine(db_url)


# load all the data into a datafame by joining the tables
query = text('''
Select * 
FROM "RawRecords" as r
JOIN "CalculatedStats" AS cs ON cs."RecordId"=r."Id";
''')
df = pd.read_sql_query(query,con=engine)
df.set_index('Id', inplace=True)
df

# # K-Means

import pandas as pd
from sklearn.cluster import KMeans


model_df = df[[
    "AvgMath4Score",
    "AvgMath8Score",
    "AvgReading4Score",
    "AvgReading8Score",
    "FederalFundingPercent",
    "StateFundingPercent",
    "LocalFundingPercent",
    "RevenuePerStudent",
    "InstructionalExpensePercent"
]]
model_df.index = df.index
model_df

#scaling math scores and YEAR columns
scaler = StandardScaler()
scaled_data = scaler.fit_transform(model_df)
scaled_df = pd.DataFrame(scaled_data, index=df.index, columns=list(model_df.columns))

# Initializing model with K = 3
model = KMeans(n_clusters=3, random_state=5)

# Fitting model
model.fit(scaled_df)

# Get the predictions
predictions = model.predict(scaled_df)

# Add clusters to dataframe
df['Cluster'] = model.labels_

# drop the Clusters table if it already exists
try:
    with engine.connect() as con:

        rs = con.execute(text('DROP TABLE "Clusters";'))
except:
    print("drop table failed")


# rename the index
df.index.rename('RecordId', inplace=True)
# store in the database
con = engine.connect()
table_name = 'Clusters'
df[['Cluster']].to_sql(table_name, con)

df.to_json(r'Resources/output.json', orient='records')
