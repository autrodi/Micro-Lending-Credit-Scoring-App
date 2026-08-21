# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Define constraints for wrapping models
def identify(y):
    return y

def apply_constraints(y):
    return np.clip(y, 300, 850).astype(int)

# load pickle files
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('std_scaler.pkl')
hot_encoder = joblib.load('hot_encoder.pkl')
ord_encoder = joblib.load('ord_encoder.pkl')

# App title
st.title('Credit Scoring App')
st.write(
    'A micro-lending app for credit scoring and evaluating' + 
    ' requests for micro-loans.')

# Data input fields
location = st.selectbox(
    '1. Location: \n\nDo you stay in an Urban, Semi-Urban, Rural area?',
    ['Urban', 'Semi-Urban', 'Rural']
)
annual_income = st.number_input(
    '2. Annual Income: \n\nHow much do you earn in a year? For earnings ' + 
    f'between {chr(8358)}50,000 and {chr(8358)}12,000,000', min_value=50000.00, 
    max_value=12000000.00, value=870000.00, step=1000.00, format='%.2f'
)
age = st.number_input(
    '3. Age: \n\nHow old are you? NB persons either below 20 years or above' + 
    ' 65 years are not eligible!', min_value=20, max_value=65, value=32, 
    step=1, format='%d'
)
marital_status = st.selectbox(
    '4. Marital Status: \n\nSelect \'Otherwise\' if status still single' + 
     ' or if no longer married (by divorce or demise)',
    ['Married', 'Otherwise']
)
household_dependents = st.number_input(
    '5. Household Size: \n\nHow many dependants do you support in total' + 
    ' including children, spouces, relatives and domestic workers?',
    min_value=0, max_value=15, value=4, step=1, format='%d'
)
telecom_monthly_spend = st.number_input(
    f'6. Mobile Expenses: \n\nHow much do you spend (in {chr(8358)}) monthly ' + 
    'average on your gadgets? airtime, data, VAS or in-app subscriptions?', 
    min_value=100.00, max_value=80000.00, value=4900.00, step=100.00, format='%.2f'
)
betting_monthly_freq = st.number_input(
    '7. Gaming Activities: \n\nOn how many days in a month do you play bets, ' + 
    'pools or ticket draws whether physically or via virtual gaming platforms?', 
    min_value=0, max_value=31, value=4, step=1, format='%d'
)
betting_monthly_spend = st.number_input(
    f'8. Gaming Expenses: \n\nPlease estimate how much do you spend (in {chr(8358)})' + 
    ' monthly average on gaming platforms. Indicate 0 if not applicable!', 
    min_value=0.00, max_value=500000.00, value=5400.00, step=100.00, format='%.2f'
)
lending_app_active = st.selectbox(
    '9. Lending Activities: \n\nAre you active on any lending apps or platform?' + 
     ' Select \'Inactive\' if not applicable!',
    ['Active', 'Inactive']
)

st.write(
    'GRADING CRITERIA:\n\n - Tier 1: 740 to 850 points\n - Tier 2: 630 to 739 ' + 
    'points\n - Tier 3: 520 to 629 points\n - Tier 4: 300 to 519 points\n')

# Derived fiels
earning_bracket = [
    'Destitute' if annual_income < 250000 else 
    'Vulnerable' if annual_income < 600000 else 'Transitional' 
    if annual_income < 1200000 else 'Lower Middle' 
    if annual_income < 3000000 else 'Upper Middle'
][0]
parity_ppp = [
    round(annual_income / 250, 2) * {
        'Rural': 1.5, 'Urban': 0.5, 'Semi-Urban': 1}[location]
][0]

# Define decision criteria
def assign_risk_tier(score):
    '''Arbitrary ratio of amount available to applicant'''
    # Prime lenders to be availed up to 40% of annual income 
    if score >= 740: return (
        'Tier 1', 'Prime Lender', 
        'Auto-Approve with Minimal Verificaton, Maximum Limit, Low' + 
        ' Interest, Direct Disbursement, Third-party Security Desirable', 0.4)
    # Standard lenders to be availed up to 30% of annual income 
    if score >= 630: return (
        'Tier 2', 'Standard Lender', 
        'Approve with Verification, Revised Limit, Moderate Interest' + 
        ', Direct and Indirect Disbursment, Third-party Security Desirable', 0.3)
    # Watchlisted lenders to be availed not more than 20% of annual income 
    if score >= 520: return (
        'Tier 3', 'Watchlisted', 
        'Exceptional Approval with Verification, Low Limit, High Interest, ' +
        'No Cash Disbursement, Third-party Security Required', 0.2)
    # Decclined requests not to be availed micro-credit 
    return (
        'Tier 4', 'Below Par', 
        'Decline (High Default Probability)', 0)

# Predict Credit Score
if st.button('Evaluate Credit Score'):
    # Data
    data = pd.DataFrame({
        'location': [location], 'earning_bracket': [earning_bracket], 
        'annual_income': [annual_income], 'parity_ppp': [parity_ppp],
        'age': [age], 'marital_status': [marital_status], 
        'household_dependents': [household_dependents], 
        'telecom_monthly_spend': [telecom_monthly_spend], 
        'betting_monthly_freq': [betting_monthly_freq], 
        'betting_monthly_spend': [betting_monthly_spend], 
        'lending_app_active': [lending_app_active]
    })
    
    # Evaluate Credit Score
    credit_score = model.predict(data)
    eligible_amount = annual_income * assign_risk_tier(credit_score)[3]
    
    # Display the Score

    st.success(
        f'SCORE CARD:\n\n - CREDIT SCORE: {credit_score[0]} points\n' + 
        f' - GRADE: {assign_risk_tier(credit_score)[0]}\n' + 
        f' - LENDER PROFILE: {assign_risk_tier(credit_score)[1]}\n' + 
        f' - CREDIT CRITERIA: {assign_risk_tier(credit_score)[2]}\n' +
        f' - RATIO CAP: {assign_risk_tier(credit_score)[3]:.0%} ' + 
        'Loan-to-Income Ratio\n' +
        f' - ELIGIBLE AMOUNT: Maxium {chr(8358)}{eligible_amount:,.2f}'
    )
