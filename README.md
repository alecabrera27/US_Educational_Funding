# An exploration into K-12 education funding revenue and expenditures on state average test outcomes.

## Overview

Utilizing a dataset from Kaggle, we are investigating if there is a relationship between the revenue and expeditures of a state on education and their average NAEP Math/Reading exam scores.  

## Rationale

We understand that each state represented within the dataset receives a different level of revenue with respect to their federal, state and local funding streams. Further, we also understand that each state has a different level of spending as it relates to instruction, support services, capital outlay and other items. Understanding then that because there are different levels of funding/expenditures, we are looking to explore if there exists trends that can be derived from the data with respect to the outcomes of the students within the state. By exploring this, we will be able to create a template to inform future practices as it relates to the funding and spending of states on their education. 

## Stakeholders

As the dataset (and subsequent analysis) is focused on stakeholders that will be able to influence funding and expenditures at a state level. Therefore, the superintendents and other school officials are the stakeholders that we are targeting with our analysis. 

## Scope

To ensure that our exploration of data is specific and measurable, we will be looking exclusively at the National Assessment of Education Progress (NAEP) Math and Reading scores for 4th and 8th grade. As the NAEP assessment is a congresionnally mandated project that is conducted nationwide, it will likely provide the best data for comparison across states. 

## Dataset Utilized

We are utilizing the following [data set](https://www.kaggle.com/noriuk/us-education-datasets-unification-project).

By performing an exploratory data analysis, we have found the following columns contained in the data that is pertinent to our exploration: 

* Demographic Information
 * Year
 * State
 * Enrolled
* Financial Information
  * Total Revenue
   * Federal Revenue
   * State Revenue
   * Local Revenue
 * Instruction Expenditure
 * Support Services Expenditure
 * Capital Outlay Expenditure
 * Other Expenditure
* Student Outcomes
 * Average National Assessment of Educational Progress Math Scores (4th & 8th Grade)
 * Average National Assessment of Educational Progress Reading Scores (4th & 8th Grade)

## Questions we are seeking to answer

The team is specifically interested in looking at exploring the following:

* Are there correlations between funding and/or expenditures and the average state NAEP Math/Reading scores for 4th and 8th grade?
* How do funding and expenditures of higher performing states (as defined by higher average NAEP Math/Reading scores) compare to states that are lower performing?

By exploring the questions, we hope to provide advice/guidance to states as they advocate for funding or spend dollars on school budgets. 

## Team Makeup

Considering the scope of the project, a team has been formed that comprises of the following individuals: 

* Alejandra Alvarez
* Eric Dalley
* Kenny Priester
* Joel Robles

To ensure fluid communication between the indivdiual team members, the following teechnologies for communication will be utilized:

* Slack
* Phone

The team will meet up as needed to discuss steps within the project and lend assistance to each other as necessary. 

## Technologies Utilized

As this project is taking a large amount of data from across a range of years (and further exploring and understanding relationships), the team has decided to create a database. After importing the CSV file from Kaggle and cleaning it up, the database will utilize the following structure:

![ERD](https://github.com/alecabrera27/US_Educational_Funding/blob/2c5d926815fdb3d2c888222079267cbc9b296c00/Resources/Images/ERD.png)

The team will be utilizing PostgreSQL during this step.

After the database has been completed, the team will utilize Python 3.7 and the following libraries/packages:

* NumPy
* SciPy
* Scikit-learn
* Plotly
* hvplot
* imbalanced-learn
* TensorFlow

By utilizing the libraries/packages above, the team will be well set up to utilize an unsupervised machine learning model. 

Finally, in the presentation of the data and results, the team will utilize the following technologies:

* Tableau
* GitHub

## Data Exploration

To begin the data exploration portion of the project, the team focused on creating the database that would be utilized to access the static data (i.e., the Kaggle dataset) that will be utilized during the scope of the project. As noted in the Technologies Utilized section, the team conceptualized three tables:

![ERD](https://github.com/alecabrera27/US_Educational_Funding/blob/2c5d926815fdb3d2c888222079267cbc9b296c00/Resources/Images/ERD.png)

Utilizing SQL, the team created the file - schema.sql to create the following tables:

```
CREATE TABLE "BaseRecord" (
    "Id" int   NOT NULL,
    "Year" int   NOT NULL,
    "State" string   NOT NULL,
    CONSTRAINT "pk_BaseRecord" PRIMARY KEY (
        "Id"
     )
);

REATE TABLE "Financials" (
    "RecordId" int   NOT NULL,
    "Enrolled" int   NOT NULL,
    "TotalRevenue" int   NOT NULL,
    "FederalRevenue" int   NOT NULL,
    "StateRevenue" int   NOT NULL,
    "LocalRevenue" int   NOT NULL,
    "InstructionExpenditure" int   NOT NULL,
    "SupportServicesExpenditure" int   NOT NULL,
    "CapitalOutlayExpenditure" int   NOT NULL,
    "OtherExpenditure" int   NOT NULL,
    CONSTRAINT "pk_Financials" PRIMARY KEY (
        "RecordId"
     )
);

CREATE TABLE "Achievements" (
    "RecordId" int   NOT NULL,
    "AvgMath4Score" int   NOT NULL,
    "AvgMath8Score" int   NOT NULL,
    "AvgReading4Score" int   NOT NULL,
    "AvgReading8Score" int   NOT NULL,
    CONSTRAINT "pk_Achievements" PRIMARY KEY (
        "RecordId"
     )
);

```
    
After some additional edits, the next step for the team was to create a database engine and utilize the schema.sql file:

```
# create database engine
db_url = f"postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
engine = create_engine(db_url)

# create schema if not already created
path = "schema.sql"
file = open(path)
escaped_sql = text(file.read())
engine.execute(escaped_sql)
```

Taking our base table, we dropped all NA values:

```
clean_df = base_df.dropna()
clean_df
```

From the cleaned dataframe, we were then able to create our three tables:

```
base_table = clean_df.rename(columns = {'PRIMARY_KEY':'Id', 'STATE':'State', 'YEAR':'Year'})[['Id', 'State', 'Year']]

fin_table = clean_df.rename(columns = {
    'PRIMARY_KEY':'RecordId', 
    'ENROLL':'Enrolled',
    'TOTAL_REVENUE':'TotalRevenue', 
    'FEDERAL_REVENUE':'FederalRevenue',
    'STATE_REVENUE':'StateRevenue',
    'LOCAL_REVENUE':'LocalRevenue',
    'TOTAL_EXPENDITURE':'TotalExpenditure',
    'INSTRUCTION_EXPENDITURE':'InstructionExpenditure',
    'SUPPORT_SERVICES_EXPENDITURE':'SupportServicesExpenditure',
    'CAPITAL_OUTLAY_EXPENDITURE':'CapitalOutlayExpenditure',
    'OTHER_EXPENDITURE':'OtherExpenditure'})[[
    'RecordId', 
    'Enrolled', 
    'TotalRevenue', 
    'FederalRevenue', 
    'StateRevenue',
    'LocalRevenue',
    'TotalExpenditure',
    'InstructionExpenditure',
    'SupportServicesExpenditure',
    'CapitalOutlayExpenditure',
    'OtherExpenditure'
]]

ach_table = clean_df.rename(columns = {
    'PRIMARY_KEY':'RecordId', 
    'AVG_MATH_4_SCORE':'AvgMath4Score',
    'AVG_MATH_8_SCORE':'AvgMath8Score',
    'AVG_READING_4_SCORE':'AvgReading4Score',
    'AVG_READING_8_SCORE':'AvgReading8Score',})[[
    'RecordId', 
    'AvgMath4Score', 
    'AvgMath8Score', 
    'AvgReading4Score', 
    'AvgReading8Score'
]]

```

And finally, store these tables in the database:

```
# store base_table in the database
con = engine.connect()
table_name = 'BaseRecord'
base_table.to_sql(table_name, con)

# store fin_table in the database
table_name = 'Financials'
fin_table.to_sql(table_name, con)

# store ach_table in the database
table_name = 'Achievements'
ach_table.to_sql(table_name, con)
```

By utilizing AWS, the team could now create a database engine and load the data into a dataframe by joining the tables:

```
# create database engine
db_url = f"postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
engine = create_engine(db_url)

# load all the data into a datafame by joining the tables
query = text('''
SELECT 
    b."Id",
    b."State",
    b."Year",
    f."Enrolled",
    f."TotalRevenue",
    f."FederalRevenue",
    f."StateRevenue",
    f."LocalRevenue",
    f."InstructionExpenditure",
    f."SupportServicesExpenditure",
    f."CapitalOutlayExpenditure",
    f."OtherExpenditure",
    ach."AvgMath4Score",
    ach."AvgMath8Score",
    ach."AvgReading4Score",
    ach."AvgReading8Score"
FROM "BaseRecord" AS b
JOIN "Financials" AS f ON f."RecordId"=b."Id"
JOIN "Achievements" AS ach ON ach."RecordId"=b."Id";
''')
df = pd.read_sql_query(query,con=engine)

```

With these steps completed, the team began loading in dependencies to create the machine learning model:

```
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

import hvplot.pandas
from sklearn.cluster import KMeans
```

As the team began their analysis, the team decided to only focus on the 4th grade math scores for each state as a starting point for the data analysis. To begin, with the dataframe (df), the team created a 2nd dataframe with only the Average 4th grade math scores for each state:

```
#Creating DataFrame with necessary information
df2 = df[['AvgMath4Score']]

```

And, from there, added in funding percentages, revenue per student, and instructional expense per student to the dataframe:

```
#Adding funding percentages to dataframe

federal_percent = df['FederalRevenue']/df['TotalRevenue']
state_percent = df['StateRevenue']/df['TotalRevenue']
local_percent = df['LocalRevenue']/df['TotalRevenue']

Revenue_per_student = df['TotalRevenue']/df['Enrolled']
Instructional_expense_percent = df['InstructionExpenditure']/df['TotalRevenue']

df2['Federal Funding Percent'] = federal_percent
df2['State Funding Percent'] = state_percent
df2['Local Funding Percent'] = local_percent
df2['Revenue per student'] = Revenue_per_student
df2['Instructional expense percent'] = Instructional_expense_percent
```

The scores (and percentages) were then scaled:

```
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df2)
```

And then, a second dataframe (with renamed columns) was created:

```
funding_df = pd.DataFrame(scaled_data)
funding_df

#Renaming math and funding columns
funding_df = funding_df.rename(columns={0: 'AvgMath4Score',
                                        1: 'Federal Funding Percent',
                                        2: 'State Funding Percent',
                                        3: 'Local Funding Percent',
                                        4: 'Revenue per student',
                                        5: 'Instructional expense percent'
                                       })
funding_df.head()
```

With this done, the team decided to utilize an unsupervised machine learning model as outcomes are not known for the dataset itself. Further, as the team was interested in understanding higher vs. lower performing schools, the team decided to utilize K-means clustering. With this in mind, in order to determine the number of clusters to utilize, the team created an elbow curve:

```
inertia = []
k = list(range(1, 11))

# Looking for the best K
for i in k:
    km = KMeans(n_clusters=i, random_state=0)
    km.fit(funding_df)
    inertia.append(km.inertia_)

# Define a DataFrame to plot the Elbow Curve using hvPlot
elbow_data = {"k": k, "inertia": inertia}
df_elbow = pd.DataFrame(elbow_data)
df_elbow.hvplot.line(x="k", y="inertia", title="Elbow Curve", xticks=k)
```

Based on the data, the team utilized k = 3 for the analysis of data and began initializing, fitting and getting predictions for the dataset:

```
# Initializing model with K = 3
model = KMeans(n_clusters=3, random_state=5)

# Fitting model
model.fit(funding_df)

# Get the predictions
predictions = model.predict(funding_df)
```

Finally, the predictions were appended to the funding_df dataframe:

```
# Add clusters to funding dataframe
funding_df["cluster"] = model.labels_
funding_df.head()

#adding back to df2
df2['cluster'] = model.labels_
df2.head()
```

And the counts for each cluster were gathered:

```
funding_df["cluster"].value_counts()
```

Where the following was found:

```
0: 178
1: 172
2: 7
```

After this step was completed, the team created the following plots based on how math scores compared to percentages of funding:


In reviewing the plots, and from the clusters themselves, the team noticed one clear outlier:

```
df['cluster'] = model.labels_
df.loc[df['cluster'] == 2]
```

From here, the team identified the District of Columbia as a clear outlier in the dataset. 


## Presentation

For more information about the project: [Google Presentation](https://docs.google.com/presentation/d/1d_G04I7wVxt63fc7vXfgrIN7g2eSGCPtO8QhitXe3w4/edit?usp=sharing)

