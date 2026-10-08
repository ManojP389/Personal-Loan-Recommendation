import streamlit as st
import streamlit_lottie as stl
import pandas as pd
from utils import (
    generate_amortization_schedule, generate_pdf
)
from agent import process_loan_application
from pathlib import Path

# Set page config and theme
st.set_page_config(
    page_title="Satya Bank Loan Origination",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
.reportview-container {background-color: #f4f7fa;}
.sidebar .sidebar-content {background-color: #ffffff;}
</style>
""", unsafe_allow_html=True)

# Sidebar - Loan Application Form
st.sidebar.header("Loan Application")
with st.sidebar.form("loan_form"):
    name = st.text_input("Customer Name", placeholder="Enter full name")
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    income = st.number_input("Annual Income (USD)", min_value=10000.0, value=50000.0, step=1000.0)
    amount = st.number_input("Loan Amount (USD)", min_value=1000.0, value=10000.0, step=500.0)
    purpose = st.selectbox("Purpose", ["Home", "Car", "Education", "Business", "Personal"])
    submitted = st.form_submit_button("Submit")

# Main Panel
st.title("Enterprise AI-Powered Loan Origination System")
st.write("Welcome to Satya Bank's cutting-edge loan processing platform. Fill in the form on the left and submit to proceed.")

if submitted:
    if not name:
        st.error("Please enter the customer's name.")
    else:
        # Show processing spinner
        with st.spinner("Analyzing application..."):
            result = process_loan_application(name, age, income, amount, purpose)

        # Display LLM-generated summary
        st.subheader("Loan Committee Summary")
        st.info(result['summary'])

        # Key Metrics
        cs = result['credit_score']
        risk = result['risk']
        offer = result['offer']
        approved = result['approval']['status']
        reason = result['approval']['reason']

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Credit Score", cs)
        col2.metric("Risk Level", risk)
        col3.metric("Interest Rate", f"{offer['rate']}%")
        col4.metric("Approval", "Approved" if approved else "Declined", help=reason)

        # Amortization Schedule Chart
        st.subheader("Amortization Schedule")
        df_schedule = generate_amortization_schedule(amount, offer['rate'], offer['tenure_years'])
        # Interactive Plotly chart with markers and hover
        import plotly.express as px
        fig = px.line(df_schedule, x='Month', y='Balance', title='Loan Balance Over Time', markers=True)
        st.plotly_chart(fig, use_container_width=True)
        # Show success animation for approved loans
        if approved:
            lottie_path = Path("assets/lottie_success.json")
            with open(lottie_path, "r") as f:
                lottie_success = f.read()
            stl.st_lottie(lottie_success, height=200)

        # Downloadable PDF proposal
        st.subheader("Download Loan Proposal")
        pdf_file = generate_pdf(result)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name="Loan_Proposal.pdf", mime="application/pdf")