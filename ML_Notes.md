# Machine Learning Notes:

* Possible Models: K-Means (unsupervized), Basic Regression, Decision Tree Regression, and KNN (supervized)

## K-Means (unsupervized):

* Starting with kmeans to better understand what relationships exist within the data. How many clusters we should use is still uncertain. To help determine the clusters, an elbow curve may be helpful. 

Input:
* 1-hot encodings for the Year (Year_1990, Year_1991, etc)
* 1-hot encodings for the state (State_TX, State_LA, etc)
* Revenue ratios: Total, Federal, State, Local
* avg math 4 score (still thinking about how to combine scores for both grades)
* avg math 8 score 
* avg reading 4 score
* avg reading 8 score

Output:
* cluster classifier


## Basic Regression:

* plot a linear regression for all revenue ratios and compare the accuracies
* May provide clearer results. For example, we could show that there is a X% confidence there is a positive correlation between funding per student and performance.

## Decision Tree Regression


## KNN (supervized)

* We could translate the raw scores to classifiers “Basic”, “Proficient”, and “advanced” and use KNN to try and predict that classification from the other variables


## Questions to think about:

* Which model was chosen and why?
* How should the model be trained?
* What is the modules accuracy?
* How does the model work?
* Is a supervized or unsupervized model better for this project?

