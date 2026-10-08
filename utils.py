import random
import pandas as pd
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from jinja2 import Environment, FileSystemLoader
import os

# 1️⃣ Credit score simulation (simple model: base 300 + income/1000 + age/2 + random noise)
def generate_credit_score(age: int, income: float) -> int:
    base = 300 + (income / 1000) + (age / 2)
    return min(int(base + random.uniform(-50, 50)), 850)

# 2️⃣ Risk assessment
def assess_risk(credit_score: int, amount: float, income: float) -> str:
    ratio = amount / (income * 5)
    if credit_score > 700 and ratio < 0.5:
        return "Low"
    elif credit_score > 600 and ratio < 1:
        return "Medium"
    else:
        return "High"

# 3️⃣ Offer recommendation
def recommend_offer(risk: str) -> dict:
    if risk == "Low":
        return {"rate": 7.5, "tenure_years": 5}
    elif risk == "Medium":
        return {"rate": 12.0, "tenure_years": 3}
    else:
        return {"rate": 18.0, "tenure_years": 1}

# 4️⃣ Approval decision
def assess_approval(risk: str) -> tuple[bool, str]:
    approved = (risk == "Low" or risk == "Medium")
    reason = "Approved" if approved else "Declined due to high risk"
    return approved, reason

# 5️⃣ Amortization schedule
def generate_amortization_schedule(principal: float, rate: float, years: int) -> pd.DataFrame:
    """
    Generates an amortization schedule as a DataFrame with columns Month and Balance.
    """
    monthly_rate = rate / 100 / 12
    n_months = years * 12
    balance = principal
    # Fixed monthly payment using annuity formula
    payment = principal * (monthly_rate * (1 + monthly_rate)**n_months) / ((1 + monthly_rate)**n_months - 1)
    records = []
    for m in range(1, n_months + 1):
        interest = balance * monthly_rate
        principal_paid = payment - interest
        balance -= principal_paid
        records.append({"Month": m, "Balance": max(balance, 0)})
    return pd.DataFrame(records)

# 6️⃣ PDF proposal generator
def generate_pdf(data: dict, filename: str = "loan_proposal.pdf") -> str:
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('loan_proposal.html')
    html = template.render(data=data)
    c = canvas.Canvas(filename, pagesize=LETTER)
    text = c.beginText(40, 750)
    for line in html.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.save()
    return os.path.abspath(filename)