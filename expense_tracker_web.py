import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#File path
CSV_FILE = "expenses.csv"

#To load existing data
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

st.title("Expense Tracker")

with st.form("expense_form"):
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Food", "Transport", "Clothes", "Savings", "School", "Other"])
    with col2:
        description = st.text_input("Description")
        date = st.date_input("Date", datetime.today())

    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_data = {"Date": date.strftime("%Y-%m-%d"), "Category": category,
                "Description": description, "Amount": amount}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.success(f"Added: {category} - {description} - ₦{amount:.2f}")
st.subheader(f"Total Spent: ₦{df['Amount'].sum():.2f}")
st.dataframe(df)

st.subheader("Summary by Category")
category_summary = df.groupby("Category")["Amount"].sum()
st.bar_chart(category_summary)

st.subheader("Monthly Spending")
df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
monthly_summary = df.groupby("Month")["Amount"].sum()
st.line_chart(monthly_summary)