import streamlit as st
import joblib
import pandas as pd
import datetime
import json
from big_query import BigQuery



st.title("Welcome to ABC Bank")

model = joblib.load('model_final.joblib')
#Even though we are not going to use gender to predict the loan status,
#we will be getting the gender data for future plans/schemes.
with st.form('Loan Form',clear_on_submit=True):
    col1,col2 = st.columns(2)
    with col1:
        Gender = st.selectbox('Gender',('Male','Female'))
        Applicant_Income = st.number_input('Applicant Income',min_value=15000)
        Coapplicant_Income = st.number_input('Co-applicant Income',min_value=0)
        Loan_amount = st.number_input('Loan Amount (In Lakhs)',min_value=2)
        Loan_Amount_Term = st.number_input('Loan Amount Term (Months)',min_value=12)
    with col2:
        Property_Area = st.selectbox('Property Area',('Urban','Rural','Semiurban'))
        Credit_History = st.number_input('Credit History',min_value=0,max_value=1)
        Self_Employed = st.selectbox('Self Employed',('Yes','No'))
        Dependents = st.selectbox('Dependents',('0','1','2','3+'))
        Education = st.selectbox('Education',('Graduate','Not Graduate'))
        Married = st.selectbox('Married',('Yes','No'))

    df = pd.DataFrame({
        'Married': [Married],
        'Dependents': [Dependents],
        'Education': [Education],
        'Self_Employed': [Self_Employed],
        'Applicant_Income': [Applicant_Income/100],
        'Coapplicant_Income': [Coapplicant_Income/100],
        'Loan_Amount': [Loan_amount],
        'Loan_Amount_Term': [Loan_Amount_Term],
        'Credit_History': [Credit_History],
        'Property_Area': [Property_Area]}
        )
    def emi_calculator(principle,term):
        #interest = PNR/100
        interest = (principle * 1000 * 8.5 * term )/float(12*100)
        emi = ((principle*1000) + interest)/term
        return emi
    df['EMI'] = df.apply(lambda row: emi_calculator(row['Loan_Amount'],row['Loan_Amount_Term']),axis =1)
    df['EMI'] = round(df['EMI'],2)
    df['Balance_Income'] = (df['Applicant_Income'] + df['Coapplicant_Income']) - df['EMI']
    df['Balance_Income'] = round(df['Balance_Income'],2)
    


    submit = st.form_submit_button('Predict')
    if submit:
        prediction = model.predict(df.drop(columns = ['Applicant_Income','Coapplicant_Income','Loan_Amount','Loan_Amount_Term']))
        df['Gender'] = Gender
        df['_created_at'] = datetime.datetime.now()
        df['_created_by'] = 'user'
        df['Approval_Id'] = df['_created_by']+'-'+df['_created_at'].astype('str')
        df['Prediction'] = prediction
        bg=BigQuery()
        bg.load_data(df)
        if prediction:
    
            st.success(f'Congratulations, Your Home Loan is Approved!!')
        else:
            st.error('We are extremely sorry to inform you that you Home Loan is not approved. Please reach out to nearest branch for further clarification')

