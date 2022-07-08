import streamlit as st
import requests
from PIL import Image

st.set_page_config(
    page_title="Churn Predictor",
    page_icon="📱",
    layout="centered",
    menu_items={
        'Get Help': 'https://www.github.com/nabilaedelliana',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is My Fist Machine Learning Online Apps!"
    }
)

st.markdown("<h1 style='text-align: center; color: black;'>Telco Customer Churn Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>This is a free online apps to predict telco customer churn whether they will stay or leave</h4>", unsafe_allow_html=True)

image = Image.open("churn.png")
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image(image, use_column_width='always')
with col3:
    st.write(' ')

st.markdown("Predicting churn risks of our customer helps us to be more prepared for the probability of customer churn and to keep customer retention.")
st.markdown("This apps is developed with the stucture of ANN deep learning with quality up to 95%.")
# for labelling values of SeniorCitizen as option in the selectbox
SeniorCitizen_format = {0:"No",1:"Yes"}
def sc_format(option):
        return SeniorCitizen_format[option]
    
# Placement
col11, col12 = st.columns(2)
with col11:
    st.subheader("Senior Citizen")
    SeniorCitizen = st.selectbox("Senior Citizen (age > 65)", options=list(SeniorCitizen_format.keys()),format_func=sc_format)
with col12:
    st.subheader("Partner")
    Partner = st.selectbox("Has Partner?", ['No','Yes'])

col21, col22 = st.columns(2)
with col21:
    st.subheader("Dependents")
    Dependents = st.selectbox("Has Dependents?", ['No','Yes'])
with col22:
    st.subheader("Tenure")
    tenure = st.number_input("Tenure in month")

col31, col32 = st.columns(2)
with col31:
    st.subheader("Phone Service")
    PhoneService = st.selectbox("Has Phone Service?", ['No','Yes'])
with col32:
    st.subheader("Internet Service ")
    InternetService = st.selectbox("Has Internet Service?", ["DSL", "Fiber optic", "No"])

col41, col42 = st.columns(2)
with col41:
    st.subheader("Contract")
    Contract = st.selectbox("Select Contract",["Month-to-month", "One year", "Two year"])
with col42:
    st.subheader("Paperless Billing")
    PaperlessBilling = st.selectbox("Has Paperless Billing?", ['No','Yes'])

col51, col52 = st.columns(2)
with col51:
    st.subheader("Payment Method")
    PaymentMethod = st.selectbox("Select Payment Method", ["Electric check","Mailed Check","Bank transfer (automatic)","Credit card (automatic)"])
with col52:
    st.subheader("Monthly Charges")
    MonthlyCharges = st.number_input("Input Monthly Charges")

# inference
data = {'Senior_Citizen':SeniorCitizen,
        'Has_Partner?':Partner,
        'Has_Dependents?': Dependents,
        'Tenure_in_month':tenure,
        'Has_Phone_Service?':PhoneService,
        'Has_Internet_Service?':InternetService,
        'Select_Contract':Contract,
        'Tenure':tenure,
        'Has_Paperless_Billing?':PaperlessBilling,
        'Select_Payment_Method':PaymentMethod,
        'Input_Monthly_Charges':MonthlyCharges}

URL = "https://churn-predictor-be-ed.herokuapp.com/predict"

# komunikasi
prediction = st.button('Predict')
if prediction :
    r = requests.post(URL, json=data)
    res = r.json()

    if r.status_code == 200:
        st.markdown(res['result']['class_name'])

    elif r.status_code == 400:
        st.write("There is an Error")
        st.write(res['message'])