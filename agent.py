import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from utils import generate_credit_score, assess_risk, recommend_offer, assess_approval

load_dotenv()


# Function to generate a professional loan summary using LLM
def generate_summary(data: dict) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Set GROQ_API_KEY in the environment before submitting an application.")

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        api_key=api_key
    )

    prompt = f"""
    You are a professional banking assistant at Satya Bank.
    A customer has applied for a loan with the following details:

    Name: {data['name']}
    Age: {data['age']}
    Income: {data['income']}
    Amount Requested: {data['amount']}
    Purpose: {data['purpose']}
    Credit Score: {data['credit_score']}
    Risk Level: {data['risk']}
    Interest Rate: {data['offer']['rate']}%
    Tenure (years): {data['offer']['tenure_years']}
    Approval Status: {data['approval']['status']}
    Reason: {data['approval']['reason']}

    Write a concise, professional summary suitable for internal loan
    committee review. Include key findings and recommendations.
    """

    response = llm.invoke(prompt)
    return response.content


# Main processing function
def process_loan_application(
    name: str,
    age: int,
    income: float,
    amount: float,
    purpose: str
) -> dict:

    # 1. Compute structured values
    datastruct = {}

    datastruct['name'] = name
    datastruct['age'] = age
    datastruct['income'] = income
    datastruct['amount'] = amount
    datastruct['purpose'] = purpose

    datastruct['credit_score'] = generate_credit_score(
        age,
        income
    )

    datastruct['risk'] = assess_risk(
        datastruct['credit_score'],
        amount,
        income
    )

    datastruct['offer'] = recommend_offer(
        datastruct['risk']
    )

    approved, reason = assess_approval(
        datastruct['risk']
    )

    datastruct['approval'] = {
        'status': approved,
        'reason': reason
    }

    # 2. Generate summary via LLM
    datastruct['summary'] = generate_summary(
        datastruct
    )

    return datastruct