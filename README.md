# Data Analytics & Visualization Boot Camp - Final Project - Group 5

## Selected topic

Utilizing a dataset from Kaggle, we are investigating if there is a relationship between the revenue and expeditures of a state on education and their average NAEP Math/Reading exam scores.  

## Rationale for selecting the topic

We understand that each state represented within the dataset receives a different level of revenue with respect to their federal, state and local funding streams. Further, we also understand that each state has a different level of spending as it relates to instruction, support services, capital outlay and other items. Understanding then that because there are different levels of funding/expenditures, we are looking to explore if there exists trends that can be derived from the data with respect to the outcomes of the students within the state. By exploring this, we will be able to create a template to inform future practices as it relates to the funding and spending of states on their education as they develop their budgets. 

## Description of the source of data

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

## Questions we are seeking to answer with the data

The team is specifically interested in looking at exploring the following:

* Are there correlations between funding and/or expenditures and the average state NAEP Math/Reading scores for 4th and 8th grade?
* How do funding and expenditures of higher performing states (as defined by higher average NAEP Math/Reading scores) compare to states that are lower performing?

By exploring the questions, we hope to provide advice/guidance to states as they advocate for funding or spend dollars on school budgets. 

## Data exploration phase

After investigating the CSV file (and the respective columns contained within), the team decided to create the following ERD:

![ERD](https://github.com/alecabrera27/US_Educational_Funding/blob/8c0fa84ab39505ff5eeb0fab92385742a13b71c0/Resources/Images/ERD.png)

As noted, from the RawRecord table, in order to evaluate levels of funding (as well as understand how the data itself will be clustered), two pieces of information were missing from the original source file: Funding percentages and clustering information. Therefore, in order to fill in this missing information, the team decided to create two additional tables from the RawRecords table. 

Therefore, after creating the RawRecord in pgAdmin, the team connected to a RDS in AWS.

Utilizing the ETL.ipynb file under the database folder, the team creates a new table called "CalculatedStats" from the RawRecord table: 

```
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

```
And finally, stores the table CalculatedStats in the database:

```
# store in the database
con = engine.connect()
table_name = 'CalculatedStats'
stats_df.to_sql(table_name, con)
```

As the team continued their investigation into the data, the team decided to only focus on the 4th grade math scores for each state as a starting point for their data analysis. Utilizing the Exploratory_analysis.ipynb file, the team loaded in the CSV file and created the following scatter plots to determine if there were any initial correlations between funding percentages and average state math scores: 

![Federal Funding](https://github.com/alecabrera27/US_Educational_Funding/blob/74182678ddac662cfb973cf5d1117536392c121f/Resources/Images/federal_funding_math.PNG)

![Local Funding](https://github.com/alecabrera27/US_Educational_Funding/blob/74182678ddac662cfb973cf5d1117536392c121f/Resources/Images/local_funding_math.PNG)

![State Funding](https://github.com/alecabrera27/US_Educational_Funding/blob/74182678ddac662cfb973cf5d1117536392c121f/Resources/Images/state_funding_math.PNG)

With the scatter plots showing that there was a potential relationship between the two pieces of information, the team proceeded forward with the analysis of the data. 

## Analysis phase

### Machine Learning Model 

Now that the initial data exploration was completed, the team discussed and came to a consesus to utilizean unsupervised machine learning model. Specifically, the team was interested in utilizing k-means. 

As the team was interested in comparing the funding and expenditure statistics that may have resulted in higher and lower test scores, the team understood that there would be at least two groups. We could have just split the data set by their test scores alone and compared the other statistics. However, we recognize that there are more factors that influence the test scores than we have in our data set which could skew our comparison.

Further, the advantages of k-means were that it was:

* Simple to implement
* Scales to large data

However, two of the disadvantages that can be present included:

* Cluster outliers - While we understood that we would have at least two clusters, we did not know if there would be outliers to the clusters themselves.
* Choosing k manually (we had to utilize an elbow curve) and there is a margin of error. 

Source: [k-means advantages/disadvantages](https://developers.google.com/machine-learning/clustering/algorithm/advantages-disadvantages)

With this in mind, in order to determine the number of clusters to utilize, the team created an elbow curve:

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

![Elbow Curve](https://github.com/alecabrera27/US_Educational_Funding/blob/59303e059c0c5ea8fa1b9333cae196eaf4eed203/Resources/Images/elbow_curve.PNG)

After discussion among the team, the group decided to utilize 3 clusters.

Now, utilizing Kmeans-3-KP.ipynb, the RawRecords table was joined to the CalculatedStats table:

```
# load all the data into a datafame by joining the tables
query = text('''
Select * 
FROM "RawRecords" as r
JOIN "CalculatedStats" AS cs ON cs."RecordId"=r."Id";
''')
df = pd.read_sql_query(query,con=engine)
df.set_index('Id', inplace=True)
```

With the number of clusters already determined by the team, the model was initialized, fitted, ran and added back to the dataframe:

```
# Initializing model with K = 3
model = KMeans(n_clusters=3, random_state=5)

# Fitting model
model.fit(scaled_df)

# Get the predictions
predictions = model.predict(scaled_df)

# Add clusters to funding dataframe
scaled_df["Cluster"] = model.labels_
scaled_df.head()

#adding back to df2
df['Cluster'] = model.labels_
df.head()

```
From here, the team created the following plots from the clusters to begin to identify higher performing vs. lower performing states:

![Federal Funding](https://github.com/alecabrera27/US_Educational_Funding/blob/59303e059c0c5ea8fa1b9333cae196eaf4eed203/Resources/Images/fed_funding_math_cluster.PNG)

![Local Funding](https://github.com/alecabrera27/US_Educational_Funding/blob/59303e059c0c5ea8fa1b9333cae196eaf4eed203/Resources/Images/local_funding_math_cluster.PNG)

![State Funding](https://github.com/alecabrera27/US_Educational_Funding/blob/59303e059c0c5ea8fa1b9333cae196eaf4eed203/Resources/Images/state_funding_math_cluster.PNG)

![Instructional](https://github.com/alecabrera27/US_Educational_Funding/blob/59303e059c0c5ea8fa1b9333cae196eaf4eed203/Resources/Images/Instruction_funding_math.PNG)

![Revenue per student](https://github.com/alecabrera27/US_Educational_Funding/blob/59303e059c0c5ea8fa1b9333cae196eaf4eed203/Resources/Images/rev_per_student.PNG)

In the plots, the team noticed one clear outlier (Cluster 2). Utilizing the ```.loc``` function, the team investigated the cluster further:

![df.loc](https://github.com/alecabrera27/US_Educational_Funding/blob/59303e059c0c5ea8fa1b9333cae196eaf4eed203/Resources/Images/df_loc.PNG)

As it turns out, it appears as though the Disctrict of Columbia is a clear outlier as a result of receiving no "State" funding. 

Using the KMeans model we were able to identify 2 clusters with significantly different mean test scores, thus we used these clusters to do our comparisons

## Technologies, languages, tools and algorithms

The team has utilized the following:

Python
 * Pandas
 * numpy
 * matplotlib
 * sklearn
 * SQLAlchemy
 * Plotly

PgAdmin

Tableau

GitHub

Slack (for communication)

## Results of the analysis
After the model established by the team, the team plotted out the clusters utilizing the average math/reading scores and the percentage of funding offered by the respective sources.

The team created the following graphs:

* Math scores compared to financial data:
 * State Average 4th Grade Math
   
   * Federal funding 
   * State funding
   * Local funding
   * Revenue per student
   * Instructional expense per student
   
 * State Average 8th Grade Math
  
   * Federal funding 
   * State funding
   * Local funding
   * Revenue per student
   * Instructional expense per student

* Reading scores compared to financial data:
 * State Average 4th Grade Reading
  
   * Federal funding 
   * State funding
   * Local funding
   * Revenue per student
   * Instructional expense per student
     
 * State Average 8th Grade Reading
 
   * Federal funding 
   * State funding
   * Local funding
   * Revenue per student
   * Instructional expense per student

In addition to this, the team also created trend lines for each of the graphs to better understand the relationship present. For the trend lines, the r squared values for revenue per student, federal funding %, state funding %, and local funding % are above 10% vs all 4 test score categories. The stat with the least fit regression is Instructional expense % with r squared values of 5% or less. Based on the data present, the team drew the following conclusions.

### Federal funding

* 4th Grade Reading & Math Scores

Based on the graphs provided here (along with trend lines):

![Fourth Math](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_math_fed.PNG)

![Fourth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_read_fed.PNG)

It appears to suggest that as the percentage of federal funding rises, that the average reading and math score for the 4th grade fall. 

* 8th Grade Reading & Math Scores

Similarly, as observed for 4th graders, we see the same trend occur for the 8th grade students as well:

![Eighth Mat](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_math_fed.PNG)

![Eigth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_read_fed.PNG)

### State funding

* 4th Grade Reading & Math Score

As before, this appears to suggest that as the percentage of state funding rises, that the average math score for the 4th grade fall. 

![Fourth Math](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_math_state.PNG)

![Fourth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_read_state.PNG)

* 8th Grade Reading & Math Scores

Interestingly enough, as before, this appears to suggest that as the percentage of state funding rises, that the average reading and math score for the 4th grade fall. 

![Eighth Mat](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_math_state.PNG)

![Eigth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_read_state.PNG)

### Local funding

* 4th Grade Reading & Math Score

What was most interesting is that local funding seems to have the exact opposite effect on average reading/math scores as compared to state/local funding. Here, the data suggests that as local funding goes up, that average math scores for both fourth and eigth grade rise. 

![Fourth Math](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_math_local.PNG)

![Fourth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_read_local.PNG)

* 8th Grade Reading & Math Scores

Similarly, again, what is most interesting is that as local funding rises for 8th grade, that the overall math/reading scores rise:

![Eighth Mat](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_math_local.PNG)

![Eigth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_read_local.PNG)

### Revenue per student

* 4th Grade Reading & Math Score

Of no suprise though is the levels of the revenue per student. Here we see a relationship whereby as the revenue per student rises, the average math/reading score rise as well:

![Fourth Math](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_math_rev.PNG)

![Fourth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_read_rev.PNG)

* 8th Grade Reading & Math Scores

As with 4th grade reading/math scores, we also see the same relationship for 8th grade as well:

![Eighth Mat](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_math_rev.PNG)

![Eigth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_read_rev.PNG)

### Instructional expense per student

* 4th Grade Reading & Math Score
* 8th Grade Reading & Math Scores

Based on the results from the machine learning model, it does not appear as though there is a clear relationship between instructional expense  per student and average math/reading scores:

![Fourth Math](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_math_instruct.PNG)

![Fourth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_fourth_read_instruct.PNG)

![Eighth Mat](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_math_instruct.PNG)

![Eigth Read](https://github.com/alecabrera27/US_Educational_Funding/blob/bdc1bbc0bd8986dac3d791b96a6c2b0f0e7b881c/Resources/Images/final_eigth_read_instruct.PNG)

### Overall Analysis

Based on the graphs created, and the analysis created by the team, the data appears to suggest that local funding (as it increases) has an influence on average math/reading scores for both math and reading for states themselves.

## Recommendations for future analysis

With the understanding that state and federal funding appear to have a negative correlation, more analysis would be needed to understand why this relationship exists. Additional investigation into how federa/state funds are spent on education on the state level would likely yield insight into why the relationship appears to exist as it does.

## What we could have done differently

## Presentation/Dashboard

The teams dashboard is located here: 

[US Educational Funding](https://public.tableau.com/views/USEducationalFunding/Dashboard?:language=en-US&:display_count=n&:origin=viz_share_link)

The team utilized Tableau in order to create the dashboard of data present. The team imported the data from a JSON file and utilized scatter plots within Tableau and included custom parameters (and the implementation of a regression line) in order to create the visuals. 

The interactive elements of the dashboard include the filtering ability for the following parameters:

* Scores
 * Average 4th Grade Reading & Math Score
 * Average 8th Grade Reading & Math Scores

* Funding/Expenditure
   * Federal funding 
   * State funding
   * Local funding
   * Revenue per student
   * Instructional expense per student

The user can utilize the dashboard to create any graphic needed to present the data needed. 

For more information about the project: [Google Presentation](https://docs.google.com/presentation/d/1d_G04I7wVxt63fc7vXfgrIN7g2eSGCPtO8QhitXe3w4/edit?usp=sharing)

