# An exploration into K-12 education funding revenue and expenditures on state average test outcomes.

## Overview

Utilizing a dataset from Kaggle, we are investigating if there is a relationship between the revenue and expeditures of a state on education and their average NAEP Math/Reading exam scores.  

## Rationale

We understand that each state represented within the dataset receives a different level of revenue with respect to their federal, state and local funding streams. Further, we also understand that each state has a different level of spending as it relates to instruction, support services, capital outlay and other items. Understanding then that because there are different levels of funding/expenditures, we are looking to explore if there exists trends that can be derived from the data with respect to the outcomes of the students within the state. By exploring this, we will be able to create a template to inform future practices as it relates to the funding and spending of states on their education. 

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

* Are there correlations between funding and/or expenditures and the average NAEP Math/Reading scores for 4th and 8th grade?
* How do funding and expenditures of higher performing states (as defined by higher average NAEP Math/Reading scores) compare to states that are lower performing?

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

## Presentation

For more information about the project: [Google Presentation](https://docs.google.com/presentation/d/1d_G04I7wVxt63fc7vXfgrIN7g2eSGCPtO8QhitXe3w4/edit?usp=sharing)

