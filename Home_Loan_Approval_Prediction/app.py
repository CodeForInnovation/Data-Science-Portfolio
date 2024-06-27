import streamlit as st
import joblib
import pandas as pd

st.title("Welcome to ABC Bank")

model = joblib.load('model_final.joblib')
#Even though we are not going to use gender to predict the loan status,
#we will be getting the gender data for future plans/schemes.
with st.form('Loan Form',clear_on_submit=True):
    col1,col2 = st.columns(2)
    with col1:
        Gender = st.selectbox('Gender',('Male','Female'))
        Applicant_Income = st.number_input('Applicant Income',min_value=150)
        Coapplicant_Income = st.number_input('Co-applicant Income',min_value=0)
        Loan_amount = st.number_input('Loan Amount (In thousands)',min_value=5)
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
        'Applicant_Income': [Applicant_Income],
        'Coapplicant_Income': [Coapplicant_Income],
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
    df['Balance_Income'] = df['Applicant_Income'] + df['Coapplicant_Income'] - df['EMI']
    df.drop(columns = ['Applicant_Income','Coapplicant_Income','Loan_Amount','Loan_Amount_Term'])

    submit = st.form_submit_button('Predict')
    if submit:
        prediction = model.predict(df)
        if prediction:
            st.success('Congratulations, Your Home Loan is Approved!!')
        else:
            st.error('We are extremely sorry to inform you that you Home Loan is not approved. Please reach out to nearest branch for further clarification')

