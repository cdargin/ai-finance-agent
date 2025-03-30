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

# Streamlit UI
st.set_page_config(page_title="Echelor - AI Finance Agent", layout="centered")
st.title("📊 Echelor: Real-Time Financial Overview")

metrics = calculate_metrics(data)

# Display metrics
st.metric("💰 Cash on Hand", f"${metrics['cash']:,}")
st.metric("📈 Revenue (Mar)", f"${metrics['revenue']:,}")
st.metric("📉 Expenses (Mar)", f"${metrics['expenses']:,}")
st.metric("🔥 Burn Rate", f"${metrics['burn_rate']:,}")
st.metric("🛣️ Runway", f"{metrics['runway']} months")

# Show charts
st.subheader("📊 Revenue vs Expenses Trend")
fig, ax = plt.subplots()
ax.plot(data["month_labels"], data["monthly_revenue"], marker='o', label="Revenue")
ax.plot(data["month_labels"], data["monthly_expenses"], marker='o', label="Expenses")
ax.set_title("Monthly Revenue and Expenses")
ax.set_ylabel("Amount ($)")
ax.legend()
st.pyplot(fig)

# Generate and display AI summary
if st.button("Generate AI Financial Summary"):
    with st.spinner("Analyzing your financials..."):
        summary = generate_summary(metrics)
        st.success("Here's your summary:")
        st.markdown(f"> {summary}")

# User question box
st.markdown("---")
st.subheader("💬 Ask Echelor Anything")
user_question = st.text_input("Type your question about the financials:", placeholder="e.g., How long can we last if expenses increase?")
if st.button("Ask") and user_question:
    with st.spinner("Thinking..."):
        answer = answer_user_question(user_question, metrics)
        st.success("Here's the response:")
        st.markdown(f"> {answer}")
