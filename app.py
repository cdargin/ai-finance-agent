# -*- coding: utf-8 -*-
import streamlit as st
import openai
import datetime
import matplotlib.pyplot as plt
import os

# Load OpenAI API key from Streamlit secrets or environment
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-key")

# Mock QuickBooks data
data = {
    "bank_balance": 120000,
    "monthly_revenue": [22000, 25000, 27000],
    "monthly_expenses": [30000, 32000, 35000],
    "month_labels": ["Jan", "Feb", "Mar"]
}

# Calculate metrics
def calculate_metrics(data):
    cash = data["bank_balance"]
    revenue = data["monthly_revenue"][-1]
    expenses = data["monthly_expenses"][-1]
    burn_rate = expenses - revenue
    runway = round(cash / burn_rate, 1) if burn_rate > 0 else "N/A"
    return {
        "cash": cash,
        "revenue": revenue,
        "expenses": expenses,
        "burn_rate": burn_rate,
        "runway": runway
    }

# Generate AI summary
def generate_summary(metrics):
    prompt = f"""
    You are Echelor, a friendly CFO assistant. Based on the following financial data, write a brief summary of the company's financial health in plain, encouraging language.

    - Cash on hand: ${metrics['cash']}
    - Monthly revenue: ${metrics['revenue']}
    - Monthly expenses: ${metrics['expenses']}
    - Burn rate: ${metrics['burn_rate']}
    - Runway: {metrics['runway']} months

    Highlight trends or concerns and suggest next steps.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant named Echelor."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Handle user questions
def answer_user_question(question, metrics):
    context = f"""
    The company has the following financial metrics:
    - Cash on hand: ${metrics['cash']}
    - Monthly revenue: ${metrics['revenue']}
    - Monthly expenses: ${metrics['expenses']}
    - Burn rate: ${metrics['burn_rate']}
    - Runway: {metrics['runway']} months
    """
    prompt = f"{context}\n\nUser question: {question}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful financial analyst named Echelor who answers questions clearly and concisely."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# --- Streamlit UI ---
st.set_page_config(page_title="Echelor - AI Finance Agent", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #F8F9FB;
    }
    .container {
        max-width: 960px;
        margin: 0 auto;
        padding: 2rem 1.5rem;
    }
    .card {
        background-color: white;
        padding: 2rem;
        margin-bottom: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    .metric-box {
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        background-color: #F0F2F5;
    }
    h1, h2, h3, h4, h5 {
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='container'>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("📊 Echelor: Your Intelligent CFO")
st.markdown("Echelor helps you understand your financial health with real-time insights, AI-generated summaries, and simple planning tools.")
st.markdown("</div>", unsafe_allow_html=True)

# Section: Metrics
metrics = calculate_metrics(data)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🔢 Financial Snapshot")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-box'><h4>💰 Cash</h4><h2>${metrics['cash']:,}</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-box'><h4>🔥 Burn Rate</h4><h2>${metrics['burn_rate']:,}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-box'><h4>📈 Revenue</h4><h2>${metrics['revenue']:,}</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-box'><h4>🛣️ Runway</h4><h2>{metrics['runway']} months</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-box'><h4>📉 Expenses</h4><h2>${metrics['expenses']:,}</h2></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Section: Trends
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 Monthly Trends")
fig, ax = plt.subplots()
ax.plot(data["month_labels"], data["monthly_revenue"], marker='o', label="Revenue")
ax.plot(data["month_labels"], data["monthly_expenses"], marker='o', label="Expenses")
ax.set_title("Revenue vs Expenses")
ax.set_ylabel("USD")
ax.legend()
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

# Section: Summary
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🧠 Echelor's Summary")
if st.button("Generate Summary"):
    with st.spinner("Echelor is analyzing your financials..."):
        summary = generate_summary(metrics)
        st.success("Summary ready!")
        st.markdown(f"> {summary}")
st.markdown("</div>", unsafe_allow_html=True)

# Section: Scenario Planning
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🔮 Scenario Planning")
st.markdown("Test different revenue/expense levels and see how it impacts your burn rate and runway.")
col_a, col_b = st.columns(2)
assumed_revenue = col_a.number_input("Assumed Monthly Revenue ($)", value=metrics['revenue'], step=1000)
assumed_expenses = col_b.number_input("Assumed Monthly Expenses ($)", value=metrics['expenses'], step=1000)
assumed_burn = assumed_expenses - assumed_revenue
assumed_runway = round(metrics['cash'] / assumed_burn, 1) if assumed_burn > 0 else "N/A"
st.metric("📉 New Burn Rate", f"${assumed_burn:,}")
st.metric("📆 New Runway", f"{assumed_runway} months")
st.markdown("</div>", unsafe_allow_html=True)

# Section: Alerts
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🚨 Smart Alerts")
alerts = []
if metrics['cash'] < 50000:
    alerts.append("⚠️ Low cash reserves. Consider reducing spend or raising capital.")
if metrics['burn_rate'] > 30000:
    alerts.append("📛 Burn rate is high. Monitor expenses closely.")
if not alerts:
    st.success("✅ No current alerts. You're on track!")
else:
    for alert in alerts:
        st.warning(alert)
st.markdown("</div>", unsafe_allow_html=True)

# Section: Ask Echelor
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("💬 Ask Echelor")
user_question = st.text_input("Ask a financial question:", placeholder="e.g., What if revenue drops 15% next month?")
if st.button("Ask") and user_question:
    with st.spinner("Echelor is thinking..."):
        answer = answer_user_question(user_question, metrics)
        st.success("Here's the response:")
        st.markdown(f"> {answer}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
