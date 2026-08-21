# https://score-me-micro-credit-app.streamlit.app/
A micro-lending credit scoring app (MVP) that leverages regression model to develop behavioural risk-based assessment; trained on 23,000 records of synthetic data to bridge credit assessment gaps when determining micro-lending metrices of potential applicants. The app serves the working demographics comprising of low and middle income earners.

### Interface

The MVP is a one-page Q-&-A front to collect anonymous responses from individuals and return feedback on predictive credit evaluation. For compliance, the app avoids personal data (no logins, no specific information, and no data aggregation). Users are at liberty to play around with scenarios and speculate possible credit scores given the behaviour.

### Features

The Credit Scoring App relies on 9 questions only  to evaluate a credit score of potential applicants (with constraints typically at 300 and 850) and to profile applicants' eligibility for micro-finance given baseline costs and income stability. The features include:

#### Categorical data:

1. Location - Urban, Semi-Urban or Rural
2. Marital status - Married or Otherwise (single, or separated by divorce or demise of spouse)
3. Lending App Usage - Active or Inactive 

#### Numeric data:

1. Annual Income - NGN50,000.00 to NGN12,000,000.00
2. Age - 20yrs to 65yrs
3. Household dependants - up to 15
4. Monthly Telecom Expense - NGN100.00 to NGN80,000.00
5. Monthly Betting Frequency - Never to 31 days (everyday in a given month)
6. Monthly Betting Spend - NGN0.00 to NGN500,000.00

#### Derived features include: 

1. Earning Bracket - jacketed as

  - Three (3) sub-categories of low income earners

    - Below NGN250,000.00 pa
    - Next up to NGN600,000.00 pa
    - Then up to NGN1,200,000.00 pa

  - Two (2) sub-categories of middle income earners

    - Lower Middle Class (Next up to NGN3,000,000.00 pa)
    - Upper Middle Class (NGN12,000,000.00 set arbitrarily) After all, it's credit!

2. Income Parity - computed as a function of location, annual income and Purchasing Power Parity (theoretically assumed at USD250.00)

### Data generation:

Although Nigeria Data Protection Regulations jealously guard actual local credit data, the summaries of these data banks are largely available. The underlying train-test dataset is statistically reconstructed from the mean, standard deviation and skewness of each of these features broken down by earning brackets and by location. Attempts to generate 500,000 records fails to file-upload size constraints on GitHub. Only 23,000 records get the Random Forest regressor model down to size. And the performance for a million records will hold same (given that the data is synthetic)

The train-test target variable condenses these 11 features into risk factors as input for a Logistic Regression classifier. The classifier runs log-odds points calibration on the input risk factors on a scale 300 - 850 using decision function give the following criteria:

- real income (weighted by a parity quotient) 
- dependency ratio not < 0.11 real income
- telecom spend not > 0.2 nominal income
- outflow ratio not > 0.2 real income
- betting habits not > 2 per week
- lending appetite not active on lending apps

Risk-tolerance thresholds are arbitrary set because every lender sets thresholds based on each's risk acceptance criteria (subject to regulations).

### Tools

1. Scikit-learn library:
   
   - Best of 5 regression models (LinearRegression, Ridge, LogisticRegression, KNeighborsRegressor, DecisionTreeRegressor and RandomForestRegressor) the last of which was selected based on performance
   - Basic supervised machine learning model tools (train_test_split, StandardScalar and encoders)
   - Mitigating tools including pipeline, ColumnTransformer, TransformedTargetRegressor and model perfomance metrics

2. Sci-Py library: the back-bone of the underlying synthetic data stats, skewnorm and skew
3. Data handlers: numpy and pandas
4. Deployment tools: joblib and streamlit

### So What?

For the benefit of both the individual borrower and the licensed lending institution, behavioural models as such it is can be scaled with features that:

- incorporate proper data protections and security features
- present real-time client-to-machine-facing consultations
- provide robust training upgrades from live credit data pools
- encourage specialized unsupervised machine learning  
- perform predictive credit-liability computation, monitoring and post-disbursement profiling 
