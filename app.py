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
st.set_page_config(page_title="Echelor - AI Finance Agent", layout="wide")
st.markdown("""
    <style>
    .metric-box {
        border: 1px solid #E6E6E6;
        padding: 15px;
        border-radius: 10px;
        background-color: #FAFAFA;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .section {
        padding: 30px 15px 15px 15px;
        margin-bottom: 25px;
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #EEE;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Echelor: Your Intelligent CFO Agent")
st.markdown("""
Echelor helps you understand your startup's financial health in real-time with smart summaries, interactive forecasts, and proactive alerts.
""")

# Section: Key Metrics
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📌 Key Financial Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
metrics = calculate_metrics(data)
with col1: st.markdown(f"<div class='metric-box'><h4>💰 Cash</h4><h2>${metrics['cash']:,}</h2></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='metric-box'><h4>📈 Revenue</h4><h2>${metrics['revenue']:,}</h2></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='metric-box'><h4>📉 Expenses</h4><h2>${metrics['expenses']:,}</h2></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='metric-box'><h4>🔥 Burn Rate</h4><h2>${metrics['burn_rate']:,}</h2></div>", unsafe_allow_html=True)
with col5: st.markdown(f"<div class='metric-box'><h4>🛣️ Runway</h4><h2>{metrics['runway']} months</h2></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Section: Financial Trends
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📊 Financial Trends")
fig, ax = plt.subplots()
ax.plot(data["month_labels"], data["monthly_revenue"], marker='o', label="Revenue")
ax.plot(data["month_labels"], data["monthly_expenses"], marker='o', label="Expenses")
ax.set_title("Monthly Revenue vs Expenses")
ax.set_ylabel("Amount ($)")
ax.legend()
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

# Section: AI Summary
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🧠 Echelor’s Financial Summary")
if st.button("Generate Summary"):
    with st.spinner("Echelor is analyzing your data..."):
        summary = generate_summary(metrics)
        st.success("Here's your summary:")
        st.markdown(f"> {summary}")
st.markdown("</div>", unsafe_allow_html=True)

# Section: Scenario Planner
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🔮 Scenario Planning")
st.markdown("Adjust assumptions to see how they impact your runway.")
assumed_revenue = st.number_input("Assumed Monthly Revenue ($)", value=metrics['revenue'], step=1000)
assumed_expenses = st.number_input("Assumed Monthly Expenses ($)", value=metrics['expenses'], step=1000)
assumed_burn = assumed_expenses - assumed_revenue
assumed_runway = round(metrics['cash'] / assumed_burn, 1) if assumed_burn > 0 else "N/A"
col_a, col_b = st.columns(2)
col_a.metric("🧾 New Burn Rate", f"${assumed_burn:,}")
col_b.metric("📆 New Runway", f"{assumed_runway} months")
st.markdown("</div>", unsafe_allow_html=True)

# Section: Smart Alerts
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🚨 Smart Alerts")
alerts = []
if metrics['cash'] < 50000:
    alerts.append("⚠️ Low cash reserves. Consider reducing spend or raising capital.")
if metrics['burn_rate'] > 30000:
    alerts.append("📛 Burn rate is high. Monitor expenses closely.")
if not alerts:
    st.success("✅ No alerts. Your finances look healthy!")
else:
    for alert in alerts:
        st.warning(alert)
st.markdown("</div>", unsafe_allow_html=True)

# Section: User Q&A
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("💬 Ask Echelor Anything")
user_question = st.text_input("Type your question about your finances:", placeholder="e.g., How long can we last if revenue drops by 20%?")
if st.button("Ask") and user_question:
    with st.spinner("Echelor is thinking..."):
        answer = answer_user_question(user_question, metrics)
        st.success("Here's the response:")
        st.markdown(f"> {answer}")
st.markdown("</div>", unsafe_allow_html=True)
